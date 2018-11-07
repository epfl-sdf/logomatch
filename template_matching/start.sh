#!/usr/bin/env bash
#Petit script pour lancer le binz
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181107.1406

#source: 

python test1.py 





exit



sudo apt update
sudo apt -y install python-pip
sudo apt install -y python-opencv
sudo python -m pip install -U pip
sudo python -m pip install -U matplotlib


exit




#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./aspi.sh site_name user passwd \n\n"
    exit
fi

echo ---------- start aspi.sh

site=$1
agent="Mozilla/5.0"

mkdir html
cd html
#wget --user-agent="Mozilla/5.0" -E -m -e robots=off –w 10 --no-parent -X "/files,/templates,/cms/engineName" "$site"
wget -a log.txt --user-agent="Mozilla/5.0" -k -p --no-parent -T 1 -t 1 "$site"
#echo $site

