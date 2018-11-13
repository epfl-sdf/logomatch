#!/usr/bin/env bash
#petit script pour aspirer seulement le html d'une liste de sites web qui se trouvent dans un fichier .csv
#zf181029.1727
#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

echo -e " 
Afin de pouvoir garder batch_aspi en marche tout en pouvant quitter la console, il serait bien de le faire tourner dans un 'screen' avec:

screen -S batch_aspi  pour entrer dans screen
./batch_aspi.sh       pour lancer le serveur WEB dans screen
CTRL+a,d              pour sortir de screen en laissant tourner le serveur
screen -r batch_aspi  pour revenir dans screen
screen -x batch_aspi  pour revenir à plusieurs dans screen
CTRL+d                pour terminer screen
screen -list          pour lister tous les screens en fonctionement
"
read -p "appuyer une touche pour démarrer..."



echo ---------- start

INPUT=./data/urls_test.csv
#INPUT=./liste_sites.csv

OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read name ip ; do
	echo $nblines
	if [ $nblines != "0" ]
	then
		./aspi.sh "http://"$name".epfl.ch"
		./aspi.sh "https://"$name".epfl.ch"
	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS

echo -e "
il y a comme nombre de pages HTML:
"

find ./html |grep '\.html' |wc

