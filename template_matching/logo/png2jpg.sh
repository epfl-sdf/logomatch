#!/usr/bin/env bash
#Petit script pour convertir les png d'un dossier en jpg d'un autre dossier
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181112.1615

#source: 
#note: convert ../../../imgdiff/copyscreen_sans.png -fx '(r+g+b)/3' -colorspace Gray copyscreen_sans.jpg

rm jpg/*
mogrify -format jpg png/*.png
mv png/*.jpg jpg



