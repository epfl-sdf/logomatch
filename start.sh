#!/usr/bin/env bash
#Petit script pour lancer le binz
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181113.0857

#source: 
#note: convert ../../../imgdiff/copyscreen_sans.png -fx '(r+g+b)/3' -colorspace Gray copyscreen_sans.jpg

rm -Rf ./match
mkdir -p ./match/all ; mkdir -p ./match/yes ; mkdir -p ./match/no ; mkdir -p ./match/maybe

python test3.py




