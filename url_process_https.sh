#!/usr/bin/env bash
#Petit script pour voir s'il existe une url en https au lieu de http !
#si oui, propose alors d'utiliser alors l'url https

#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf190228.11003

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                                                            #demande au bash de supporter les pipe !

r=$1
r=`echo $r | sed "s/\http/https/g"`             #converti une url http en url https
r=`echo $r | sed "s/\httpss/https/g"`             #converti une url httpss en url https, bug de si l'url était déjà en https :-)

curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36" --insecure --max-time 5 $r  2>err.txt > html.txt                       #récupère le contenu HTML de la page web

#traitement des erreurs de connection au niveau du CURL
e=`cat err.txt |grep -i -e 'Failed to connect' -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"                                                                  #enlève le 1er caractère !
if [ "$e" != "" ]
then
#    echo -e "err: "$1", "$e >> err.log
    r=`echo $r | sed "s/\https/http/g"`         #converti une url https en url http

fi

echo $r


