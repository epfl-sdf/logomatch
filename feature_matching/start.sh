#!/usr/bin/env bash
#gc181128.1125

python="python3"
confile="start.conf"

usage() {
  cat | sed 's/    //' << __EOF 

    This script executes feature_matcher.py one or more times. 
    The first time on all the pages of the provided directory;
    then only on the "maybe" pages from the previous step.
    It accepts two mandatory argument:
      1. the path of the directory containing the images
      2. the path of the output directory
    The output is a directory (e.g. pippo) and a file (e.g. pippo.out).

    Optional argument:
      -h             Show usage and exit
      -p PYTHON      Specify which python exec to use. Example:
                     -p python
                     -p "docker run -v $PWD:/wd opencv"
      -f             Read the run descriptions from an external file instead of
                     using built in ones. The default is start.conf
                     The config file have one line per feature_matcher run
                     and each line is just a list of arguments for feature_matcher.
                     Default is start.conf

    Example:
      rm -rf work/ ; ./start.sh -p "docker run -v $PWD:/wd opencv" pages/2019-03-04/ work

__EOF
}

while getopts ":hp:f:" OPT; do
  [[ $OPTARG =~ ^- ]] && die "Option -$OPT requires an argument."
  case $OPT in
    :)
      die "Option -$OPTARG requires an argument."; ;;
    h)
      usage; exit; ;;
    p)
      python="$OPTARG"; ;;
    f)
      confile="$OPTARG"; ;;
  esac
done
shift $((OPTIND-1))

if [ -z "$1" -o -z "$2" ] ; then
    usage
    exit
fi

pd=$1
od=$2
apd=$(pwd)/$pd
aod=$(pwd)/$od

# Read run parameters from config file
IFS=$'\r\n' GLOBIGNORE='*' command eval "configs=(\$(grep -v '#' $confile))"

echo "pd:       $pd" >&2
echo "od:       $od" >&2
echo "confile:  $confile" >&2
i=0
while [ "x${configs[i]}" != "x" ] ; do
  cfg="${configs[i]}"
  let i=$i+1
  echo "  run $i: ${cfg}" >&2
done

# ---------------------------------------------------------------- 0 setup
# Generate logos from svg
./generate_logos.sh logos

if [ -d $od ] ; then
  echo "Output directory $od already exists. Please delete it and try again or change name"
  exit 1
fi

mkdir -p $od || (echo "Could not create output dir"; exit 1)

# Copy this file for future reference 
cp $confile $od/start.conf

# ----------------------------------------------------------------- 1 RUN

all_out=""; out=""; m=""
let i=0
while [ "x${configs[i]}" != "x" ] ; do
  cfg="${configs[i]}"
  let i=$i+1

  # Create a new set of pages with the maybe pages of last run
  if [ -n "$m" -a -n "$out" ] ; then
    pages=${m}_maybe
    pldst=../../$pd/
    [ -d $pages ] || mkdir $pages
    awk '/maybe$/{print $1;}' $out | while read p ; do
      # ln -s ../$m/maybe $pages/$p.png
      ln -s $pldst/$p.png $pages/$p.png
    done
  else
    pages=$pd
  fi

  m=$od/m$i
  out=$m.out
  all_out="$all_out $out"

  echo "$(date +%F-%R:%S) Start round $i" >&2
  echo "$python feature_matcher2.py $cfg -m $m $pages logos > $out" >&2
  $python feature_matcher2.py $cfg -m $m $pages logos > $out
  if [ "$?" != "0" ] ; then
    echo "Test failed. Stopping."
    exit
  fi

  # Each loop overwrites the output of the previous one as it is cumulative
  cat $all_out | grep -e 'yes$'   >  $od.out
  cat $all_out | grep -e 'no$'    >> $od.out
  cat $out     | grep -e 'maybe$' >> $od.out
done

exit
