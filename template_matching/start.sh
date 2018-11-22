#!/usr/bin/env bash
#Petit script pour lancer le binz
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181113.0857

#source: 
#note: convert ../../../imgdiff/copyscreen_sans.png -fx '(r+g+b)/3' -colorspace Gray copyscreen_sans.jpg

# Generate logos from svg
sh generate.sh

# scan all logos in all pages and draw matches in the match directory
# python -v -m mintt -M test6.py pages/png logo/png

# scan all logos in all pages but do not write match images
# python test6.py -m match -M pages/png logo/png
# python test6.py -m match pages/png logo/png


# True run

# First run without special treatments and large "maybe" zone
o=match1
python test6.py -m $o -y 12 -n 6 pages/all logo/png > $o.out

# Create a new set of pages with the maybe pages
[ -d pages/maybe ] || mkdir pages/maybe
awk '/maybe$/{print $1;}' $o.out | while read p ; do
  ln -s ../all/$p.png pages/maybe/
done

# Run again on maybepages with some tweaks
o=match2
python test6.py -k -p -m $o -y 12 -n 6 pages/maybe logo/png > $o.out
