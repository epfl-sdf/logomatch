#!/bin/bash
# This script executes start.sh on all the test pages, then make a summary of the result

usage() {
  cat | sed 's/    //' << __EOF 

    This script executes start.sh for every positional argument
    interpreted as the basename of a XXX.conf file that will 
    run start.sh with pages/test as pages, logos as logos,
    XXX.conf as configuration file, and XXX as output directory.
    Example:
    cp start.conf test1.conf ; ./test.sh -p "python" test1

    Optional argument:
      -h             Show usage and exit
      -p PYTHON      Specify which python exec to use. Example:
                     -p python
                     -p "docker run -v $PWD:/wd opencv"
__EOF
}

python="python3"
while getopts ":hp:" OPT; do
  [[ $OPTARG =~ ^- ]] && die "Option -$OPT requires an argument."
  case $OPT in
    :)
      die "Option -$OPTARG requires an argument."; ;;
    h)
      usage; exit; ;;
    p)
      python="$OPTARG"; ;;
  esac
done
shift $((OPTIND-1))

if [ ! -d pages/test ] ; then
  mkdir -p pages/test && rsync -av ../test_pages/ pages/test/
fi

while [ $# -gt 0 ] ; do
  cf=$(basename $1 .conf)
  shift 1
  out=${cf}_test.out
  echo "-----------------------------------------------" >> $out
  cat $cf.conf                                           >> $out
  echo "-----------------------------------------------" >> $out
  date                                                   >> $out

  ./start.sh -p "$python" -f ${cf}.conf pages/test $cf

  cat $cf.out                                            >> $out
  date                                                   >> $out
  echo "-----------------------------------------------" >> $out

  awk '
  BEGIN{n_good=0; n_bad=0; n_mb=0;}
  /maybe$/{n_mb=n_mb+1; next;}
  /^yes_.*no$|^no_.*yes$/{n_bad=n_bad+1; next;}
  /^yes_.*yes$|^no_.*no$/{n_good=n_good+1; next;}
  END{
    printf("good: %d  %5.1f     bad: %d  %5.1f     mb: %d. %5.1f\n\n", n_good, 100*n_good/NR, n_bad, 100*n_bad/NR, n_mb, 100*n_mb/NR);
  }
  ' $cf.out                                              >> $out
done
