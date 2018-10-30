#!/usr/bin/env bash
#Petit script pour juste compter le nombre de fichiers potentiel pour l'ancien logo de l'EPFL
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181030.1011

#source: 

echo ---------- cmpt_logo.sh

find html |grep -i -E 'gif|png|jpg|jpeg|svg' |grep -i logo

echo -e "
il y a comme nombre de site scannés:"
wc ./data/urls_test.csv

echo -e "
il y a comme nombre de sites actifs:"
find ./html |grep '\.html' |wc

echo -e "
il y a comme nombre de logo:"
find html |grep -i -E 'gif|png|jpg|jpeg|svg' |grep -i logo |wc





