#!/usr/bin/env bash
#petit script pour faire trier la liste des sites et supprimer les doublons
#zf190329.1611

#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "
Syntax:
./sort_sites.sh data/liste_sites.csv
"
    exit
fi

INPUT=$1
OUTPUT=`echo $1 | sed 's/.csv/_unique.csv/g'`

echo $INPUT
echo $OUTPUT
#exit

echo -e "Avant: "`cat $INPUT |wc -l`
sort -u $INPUT > $OUTPUT
echo -e "Après: "`cat $OUTPUT |wc -l`
