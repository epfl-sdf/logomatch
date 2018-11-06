#!/usr/bin/env bash
#petit script tout simple pour comparer une série d'images avec une image master
#zf181106.1545
#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/
#source: http://manpages.ubuntu.com/manpages/cosmic/en/man1/idiff.1.html

zNAME="logo_diff"
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

head -n 100 liste_images.csv > tmp_images.csv
INPUT=./tmp_images.csv
#INPUT=./liste_sites.csv

OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read name ip ; do
	echo $nblines
	if [ $nblines != "0" ]
	then
        echo $name


#		./aspi.sh "http://"$name".epfl.ch"
#		./aspi.sh "https://"$name".epfl.ch"
	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS

echo -e "

C'est terminé !
"

