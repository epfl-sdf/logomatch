#!/usr/bin/env bash
#petit script pour lancer le binz au niveau des batches
#zf190408.1002


zNAME="batch_all"
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

SITES=data/short_liste_sites.csv
URLS=data/short_liste_urls.csv

./batch_process_url.sh $SITES $URLS
./batch_screen_copy.sh $URLS

