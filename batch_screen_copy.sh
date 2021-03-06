#!/usr/bin/env bash
#petit script pour faire une copie d'écran des homes pages d'une liste de sites web qui se trouvent dans un fichier .csv
#zf190329.1744

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

zNAME="batch_copy_screen"
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
#read -p "Appuyer une touche pour démarrer $zNAME"


#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "
Syntax:
./batch_screen_copy.sh data/liste_url.csv
"
    exit
fi




echo ---------- start


rm -rf ~/.cache/mozilla/
rm ./images/*
mkdir ./images
cp /dev/null err.log
cp /dev/null redir.log

./sort_urls.sh $1
INPUT=`echo $1 | sed 's/.csv/_unique.csv/g'`


OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read site url ; do
	echo $nblines
	if [ $nblines != "0" ]
	then

echo -e "site: "$site
echo -e "url: "$url

        ./screen_copy.sh $url "./images/http_"$site".png"



	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS

