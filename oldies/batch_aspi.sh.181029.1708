#!/usr/bin/env bash
#petit script pour aspirer seulement le html d'une liste de sites web qui se trouvent dans un fichier .csv
#zf181028.1832
#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

echo ---------- start

INPUT=./urls_test.csv
#INPUT=./liste_sites.csv

OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read sites ; do
	echo $nblines
	if [ $nblines != "0" ]
	then
		./aspi.sh $sites
	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS

echo -e "
il y a comme nombre de pages HTML:
"

find ./html |grep '\.html' |wc

