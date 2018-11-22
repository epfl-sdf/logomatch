#!/usr/bin/env bash
#petit script pour créer des liens symboliques en fonction d'une liste CSV
#zf181122.1451

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/



rm -Rf ./images2
mkdir ./images2

INPUT=./resultat.181122.1448.csv
#INPUT=./tmp.csv


OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read site logo score status ; do
	echo $nblines
	if [ $nblines != "0" ]
	then


        fname1=$site".png"
        fname2=$score"_"$fname1
        
        echo -e "fname1: "$fname1
        echo -e "fname2: "$fname2

        cp images/$fname1 images2/$fname2


	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS

