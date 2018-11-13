#!/usr/bin/env bash
#petit script tout simple pour comparer une série d'images avec une image master
#zf181106.1721
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

rm -Rf ./images_result
mkdir images_result


echo "file,f1,f2,f3,f4,f5,f6,f7,f8,f9" > logo_diff.csv

head -n 1000 liste_images_name.csv > tmp.csv
INPUT=./tmp.csv
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
#        idiff imgdiff/logo_master.gif images/$name |awk '{print $4}' |tr '\n' ',' >> logo_diff.csv


        convert -resize 462X222 images/$name tmp.png


#        zcoeff=`idiff imgdiff/logo_master.png images/$name |awk '{print $4}' |tr '\n' ',' |awk -F "," '{print $4}'`
        zcoeff=`idiff imgdiff/logo_master.png tmp.png |awk '{print $4}' |tr '\n' ',' |awk -F "," '{print $2}' |head -c 6`
        echo $zcoeff
        cp images/$name images_result/$zcoeff"_"$name


#        echo "" >> logo_diff.csv


	fi
	((nblines+=1))
	echo ""
done < $INPUT
IFS=$OLDIFS

echo -e "

C'est terminé !
"

