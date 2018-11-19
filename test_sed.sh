#!/usr/bin/env bash
#Petit script pour test un sed
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181119.1120

#source: 
#note: 

cat -A tmp.txt 

cat tmp.txt |sed  "s/\r/\n/g" > tmp2.txt

cat -A tmp2.txt 



