#!/usr/bin/env bash
#Petit script pour suivre un redirect de type refresh dans un fichier HTML.
#Filtre aussi si le serveur ne répond pas
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181120.1648

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                                                                        #demande au bash de supporter les pipe !

r=$1
curl --max-time 2 $r  2>err.txt > html.txt                              #récupère le contenu HTML de la page web

#traitement des erreurs de connection au niveau du CURL
e=`cat err.txt |grep -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"                              #enlève le 1er caractère !

if [ "$e" != "" ]
then
    echo -e "err: "$1", "$e >> err.log
    r=""
else
    #traitement de la redirection faite à l'intérieur du HTML
    t1=`cat html.txt |grep -i 'http-equiv="refresh"' |grep -i 'url=' `      #récupère s'il y a une redirection dans le HTML
    if [ "`echo $t1 |grep http`" != "" ]                                    #test s'il y a une redirection
    then
        tmp=${t1#*+(url|URL)=}                                              # remove prefix ending in "url|URL="
        b=${tmp%\"*}                                                        # remove suffix starting with "
        if [ "`echo $b |grep http`" != "" ]                                 #test si c'est une url relative ou absolue
        then
            r=$b
        else
            r=$1"/"$b
        fi
        #garde une trace du site redirigé pour debug
        echo -e "redirect_html: "$1", "$r >> redir.log
        r=`./loop_url_process_header.sh $r`                                 #teste s'il y a encore des erreurs dans la nouvelle redirection
    fi
fi


#traitement des logos pris sur statics.epfl.ch
t1=`cat html.txt |grep -i -e 'www.epfl.ch/img/epfl_small' -e 'static.epfl.ch/latest/includes/epfl-header'  `            #récupère s'il y a un logo sur static.epfl.ch
if [ "`echo $t1 |grep http`" != "" ]                                        #test s'il y a un logo sur static.epfl.ch
then
    echo -e "static: "$1", "$t1 >> dyna.log
    r=""
fi


echo $r


