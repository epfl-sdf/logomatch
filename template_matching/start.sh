#!/usr/bin/env bash
#Petit script pour lancer le binz
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181126.1619

#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./start.sh source_folder destination_folder \n\n"
    exit
fi

pd=$1 
od=$2
if [ -n "$3" ] ; then
  python="$3"
else
  python="python3"
fi
echo "Using $python"

# ----------------------------------------------------------------
# Generate logos from svg
./generate.sh

lg=logo/png

o1=$od/m1
o2=$od/m2
o3=$od/m3

# TODO: fix for absolute paths
apd=$PWD/$pd

if [ -d $od ] ; then
  echo "Output directory $od already exists. Please delete it and try again or change name"
  exit 1
fi
mkdir -p $od || (echo "Could not create output dir"; exit 1)

# Copy this file for future reference 
cp $0 $od/

# ------------------------------------------------------------------- 1
# First run without special treatments and large "maybe" zone
echo "$(date +%F-%R:%S) Start first round" >&2
$python test6.py -l 0.68 -n 4 -y 14 -m $o1 $pd $lg > $o1.out
if [ "$?" != "0" ] ; then
  echo "Test failed. Stopping."
  exit
fi
cat $o1.out > $od.out
# exit  # uncomment to stop here



# ------------------------------------------------------------------- 2
# Create a new set of pages with the maybe pages
[ -d ${o1}_maybe ] || mkdir ${o1}_maybe
awk '/maybe$/{print $1;}' $o1.out | while read p ; do
  ln -s $apd/$p.png ${o1}_maybe/
done

# Run again on maybe-pages with some tweaks:
# -k correct thresholds based on number of keypoints in the logo
# -D discard points that are more than given value (180) pixels far from the center of mass
# -l relax a bit the Lowe cryterium for match seleciton 
echo "$(date +%F-%R:%S) Start second round" >&2

# $python test6.py -k --mingdist 40 --maxgdist 160 -l 0.74 -n 5 -y 8 -m $o2 ${o1}_maybe $lg > $o2.out
$python test6.py -p 8 -k --mingdist 40 --maxgdist 160 -l 0.70 -n 6 -y 12 -m $o2 ${o1}_maybe $lg > $o2.out
if [ "$?" != "0" ] ; then
  echo "Test failed. Stopping."
  exit
fi

cat $o1.out $o2.out | grep -e 'yes$' >  $od.out
cat $o1.out $o2.out | grep -e 'no$'  >> $od.out
cat $o2.out | grep -e 'maybe$'       >> $od.out
exit # uncomment to stop here



# ------------------------------------------------------------------- 3
[ -d ${o2}_maybe ] || mkdir ${o2}_maybe
awk '/maybe$/{print $1;}' $o2.out | while read p ; do
  ln -s $apd/$p.png ${o2}_maybe/
done

# Run again on maybe-pages with some tweaks
# -p split the image in three parts if score is smaller than given value (8)
echo "$(date +%F-%R:%S) Start third round" >&2
$python test6.py -p 8 -k --mingdist 40 --maxgdist 160 -l 0.74 -n 6 -y 8 -m $o3 ${o2}_maybe $lg > $o3.out
if [ "$?" != "0" ] ; then
  echo "Test failed. Stopping."
  exit
fi

cat $o1.out $o2.out $o3.out | grep -e 'yes$' >  $od.out
cat $o1.out $o2.out $o3.out | grep -e 'no$'  >> $od.out
cat $o3.out | grep -e 'maybe$'               >> $od.out
