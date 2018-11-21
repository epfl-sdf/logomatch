#!/usr/bin/env bash
#Petit script pour traiter les erreurs 40x et récupérer les redirections 30x au niveau du header HTTP
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181120.1845

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                                                        #demande au bash de supporter les pipes !

url=$1
curl --insecure --max-time 5 -Ivs $1  2>err.txt | sed "s/\r/\n/g" > header.txt                       #récupère le header HTTP

#traitement de l'erreurs de connection au niveau du CURL
e=`cat err.txt |grep -i -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"                                                              #enlève le 1er caractère !
if [ "$e" != "" ]
then
    echo -e "err: "$1", "$e >> err.log                                  #garde une trace du site en erreur pour debug
    url=""
else
    #traitement de la redirection au niveau du header HTTP
    if [ "`cat header.txt |grep -i 'HTTP/1.1 30'`" != "" ]              #test si c'est une redirection
    then
        url=`cat header.txt |grep -i 'Location: ' |awk '{print $2}'`    #récupère la redirection
        if [ "`echo -e $url |grep -i -e 'HTTP://' -e 'HTTPS://'`" = "" ]               #test si c'est une url absolue
        then
            b=$1
            if [ "${b: -1}" = "?" ]                                     #test si cela termine par ? et si oui l'enlève
            then
                b=${b::-1}
            fi
#            if [ "${b: -1}" = "/" ]                                     #test si cela termine par / et si oui l'enlève
#            then
#                b=${b::-1}
#            fi
            url=$b$url
        fi
        echo -e "redirect_header: "$1", "$url >> redir.log                     #garde une trace du site redirigé pour debug
#        curl --insecure --max-time 5 -Ivs $url 2>err.txt | sed "s/\r/\n/g" > header.txt             #récupère le nouveau le header HTTP
    fi
    #traitement de l'erreur faite niveau du header HTTP
    e=`cat header.txt |grep -i -e 'HTTP/' |grep -i -e '40' -e '50'`
    if [ "$e" != "" ]                                                   #test si c'est une erreur
    then
        url=""
        echo -e "err: "$1", "$e >> err.log                              #garde une trace du site en erreur pour debug
    fi
fi

echo $url






