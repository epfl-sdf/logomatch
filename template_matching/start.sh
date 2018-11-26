#!/usr/bin/env bash
#Petit script pour lancer le binz
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181113.0857

# TODO: make these two args for the script
pd=pages/test
od=match2

# ----------------------------------------------------------------

# Generate logos from svg
sh generate.sh
lg=logo/png

o1=$od/m1
o2=$od/m2
o3=$od/m3

# TODO: fix for absolute paths
apd=$(PWD)/$pd

[ -d $od ] || mkdir -p $od || (echo "Could not create output dir"; exit 1)

# First run without special treatments and large "maybe" zone
echo "$(date +%F-%R:%S) Start first round" >&2
python test6.py -n 5 -y 14 -m $o1 $pd $lg > $o1.out

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
python test6.py -k -D 180 -l 0.75 -n 5 -y 8 -m $o2 ${o1}_maybe $lg > $o2.out

[ -d ${o2}_maybe ] || mkdir ${o2}_maybe
awk '/maybe$/{print $1;}' $o2.out | while read p ; do
  ln -s $apd/$p.png ${o2}_maybe/
done

# Run again on maybe-pages with some tweaks
# -p split the image in three parts if score is smaller than given value (8)
echo "$(date +%F-%R:%S) Start third round" >&2
python test6.py -p 8 -k -D 180 -l 0.75 -n 6 -y 8 -m $o3 ${o2}_maybe $lg > $o3.out

grep -e 'yes$' $o1.out $o2.out $o3.out  > $od.out
grep -e 'no$'  $o1.out $o2.out $o3.out >> $od.out
grep -e 'maybe$' $o3.out               >> $od.out