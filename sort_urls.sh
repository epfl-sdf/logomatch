#!/usr/bin/env bash
#petit script pour faire trier et supprimer les doublons
#zf190327.1615

#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "
Syntax:
./sort_urls.sh data/liste_urls.csv
"
    exit
fi

INPUT=$1
OUTPUT=`echo $1 | sed 's/.csv/_unique.csv/g'`

echo $INPUT
echo $OUTPUT
#exit


echo -e "site,url" > $OUTPUT
echo -e "Avant: "`cat $INPUT |wc -l`
sort -u $INPUT >> $OUTPUT
echo -e "Après: "`cat $OUTPUT |wc -l`
