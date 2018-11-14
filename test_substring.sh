#!/usr/bin/env bash
#Petit script pour tester une extraction d'un string dans un string
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181114.1040

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

t1='<meta http-equiv="refresh" content="0;url=script/">'

tmp=${t1#*url=}   # remove prefix ending in "url="

echo -e "tmp: "$tmp

b=${tmp%\"*}   # remove suffix starting with "

echo -e "b: "$b





