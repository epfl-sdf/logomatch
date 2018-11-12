#!/usr/bin/env bash
#Petit script pour installer tout ce qu'il faut pour OpenCV sur Python
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181109.1032

#source: faut regarder aussi ceci https://pypi.org/project/opencv-contrib-python/

sudo apt update
sudo apt install -y python-pip python-opencv python-tk
sudo -H python -m pip install -U pip
sudo -H python -m pip install -U matplotlib


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

