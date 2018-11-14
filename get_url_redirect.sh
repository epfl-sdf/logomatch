#!/usr/bin/env bash
#Petit script pour suivre un redirect de type refresh dans un fichier HTML
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181114.1505

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:


t1=`curl --max-time 1 $1  2>err.txt |grep 'http-equiv="refresh"'`

tmp=${t1#*url=}   # remove prefix ending in "url="
b=${tmp%\"*}   # remove suffix starting with "
e=`cat err.txt |grep -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"      #enlève le 1er caractère !

if [ "$e" != "" ]
then
    echo -e "err: "$1", "$e >> err.log
fi

if [ "$b" != "" ]
then
    echo -e "redirect: "$1"/"$b >> redir.log
fi

echo -e $1"/"$b





