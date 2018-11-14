#!/usr/bin/env bash
#Petit script pour tester les erreurs au niveau du header HTTP
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181114.1708

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                        #demande au bash de supporter les pipe !

#récupère l'erreur dans le header HTTP
e=`curl --max-time 1 -Ivs $1  2>err.txt |grep -i -e 'HTTP/1.1 40'`

#traitement des erreurs au niveau du header

if [ "$e" != "" ]
then
    echo -e "err: "$1", "$e >> err.log
    r=""
else
    r=$1
fi

echo $r









exit


t1=`curl --max-time 1 $1  2>err.txt |grep 'http-equiv="refresh"'`

#traitement de la redirection faite à l'intérieur du HTML
tmp=${t1#*+(url|URL)=}                  # remove prefix ending in "url|URL="
b=${tmp%\"*}                            # remove suffix starting with "
if [ "`echo $b |grep http`" != "" ]     #test si c'est une url relative ou absolue
then
    r=$b
else
    r=$1"/"$b
fi

#garde une trace du site redirigé pour debug
if [ "$b" != "" ]
then
    echo -e "redirect: "$1", "$r >> redir.log
fi

#traitement des erreurs de connection au niveau du CURL
e=`cat err.txt |grep -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"                              #enlève le 1er caractère !

if [ "$e" != "" ]
then
    echo -e "err: "$1", "$e >> err.log
    r=""
fi

echo $r










