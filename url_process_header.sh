#!/usr/bin/env bash
#Petit script pour traiter les erreurs 40x et récupérer les redirections 30x au niveau du header HTTP
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181115.1415

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                                                        #demande au bash de supporter les pipes !

h=`curl --max-time 1 -Ivs $1  2>err.txt`                                #récupère le header HTTP

#traitement de l'erreurs de connection au niveau du CURL
e=`cat err.txt |grep -i -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"                                                              #enlève le 1er caractère !
if [ "$e" != "" ]
then
    echo -e "err: "$1", "$e >> err.log                                  #garde une trace du site en erreur pour debug
    url=""
else
    #traitement de la redirection au niveau du header HTTP
    if [ "`echo -e $h |grep -i 'HTTP/1.1 30'`" != "" ]                  #test si c'est une redirection
    then
        url=`echo -e $h |grep -i '< Location: ' |awk '{print $2}'`      #récupère la redirection
        echo -e "redirect: "$1", "$url >> redir.log                     #garde une trace du site redirigé pour debug
        h=`curl --max-time 1 -Ivs $url  2>err.txt`                      #récupère le nouveau le header HTTP
    fi
    #traitement de l'erreur faite niveau du header HTTP
    e=`echo -e $h |grep -i 'HTTP/1.1 40'`
    if [ "$e" != "" ]                                                   #test si c'est une erreur
    then
        url=""
        echo -e "err: "$1", "$e >> err.log                              #garde une trace du site en erreur pour debug
    fi
fi

echo $url






