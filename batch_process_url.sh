#!/usr/bin/env bash
#petit script pour faire le preprocessing d'une liste de sites web qui se trouvent dans un fichier .csv
#afin d'épurer la liste brute d'url
#zf181119.1759

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

zNAME="batch_process_url"
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
cp /dev/null err.log
cp /dev/null redir.log
cp /dev/null ./data/liste_url.csv

INPUT=./data/liste_sites.csv
#INPUT=./data/urls_test.csv


OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
while read name ip ; do
	echo $nblines
	if [ $nblines != "0" ]
	then

        site=$name".epfl.ch"
        echo -e "site: "$site


        url="http://"$site
        url=`./url_process_header.sh $url`

        if [ "$url" != "" ]
        then
            url=`./url_process_html.sh $url`
        fi

        if [ "$url" != "" ]
        then
            echo -e "url: "$url
            echo $url >> ./data/liste_url.csv
        fi








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

