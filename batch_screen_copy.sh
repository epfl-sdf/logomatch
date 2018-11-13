#!/usr/bin/env bash
#petit script pour faire une copie d'écran des homes pages d'une liste de sites web qui se trouvent dans un fichier .csv
#zf181113.1148

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

zNAME="batch_copy_screen.sh"
echo -e "

Afin de pouvoir garder $zNAME en marche tout en pouvant quitter la console, il serait bien de le faire tourner dans un 'screen' avec:

screen -S $zNAME    pour entrer dans screen
./start.sh             pour lancer le serveur WEB dans screen
CTRL+a,d               pour sortir de screen en laissant tourner le serveur
screen -r $zNAME    pour revenir dans screen
screen -x $zNAME    pour revenir à plusieurs dans screen
CTRL+d                 pour terminer screen
screen -list           pour lister tous les screens en fonctionement

"
read -p "Appuyer une touche pour démarrer $zNAME"

echo ---------- start


rm -Rf ./images
mkdir ./images



INPUT=./data/urls_test.csv.181029.1722
#INPUT=./liste_sites.csv

OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read name ip ; do
	echo $nblines
	if [ $nblines != "0" ]
	then



    echo -e $name

    ./screen_copy.sh $name".epfl.ch"






#		./aspi.sh "http://"$name".epfl.ch"
#		./aspi.sh "https://"$name".epfl.ch"





	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS


exit





echo -e "
il y a comme nombre de pages HTML:
"

find ./html |grep '\.html' |wc

