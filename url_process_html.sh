#!/usr/bin/env bash
#ATTENTION on ne traite plus les redirections HTML ! Petit script pour suivre un redirect de type refresh dans un fichier HTML.
#Filtre aussi si le serveur ne répond pas
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf190228.1933

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                                                            #demande au bash de supporter les pipe !

r=$1
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36" --insecure --max-time 5 $r  2>err.txt > html.txt                       #récupère le contenu HTML de la page web

#traitement des erreurs de connection au niveau du CURL
e=`cat err.txt |grep -i -e 'Failed to connect' -e 'Connection timed out after' -e 'Could not resolve host' `
e="${e:1}"                                                                  #enlève le 1er caractère !
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
            if [ "${b: -1}" = "?" ]                                     #test si cela termine par ? et si oui l'enlève
            then
                b=${b::-1}
            fi
            if [ "${b: -1}" = "/" ]                                     #test si cela termine par / et si oui l'enlève
            then
                b=${b::-1}
            fi
            r=$1"/"$b
        fi
        #garde une trace du site redirigé pour debug
        echo -e "redirect_html: "$1", "$r >> redir.log

#supprimé ce test le 190228.1934 car il me génère trop de problèmes lors de boucles !
#        r=`./loop_url_process_header.sh $r`                                 #teste s'il y a encore des erreurs dans la nouvelle redirection

    fi
fi

#traitement des logos pris sur un serveur centralisé
t1=`cat html.txt |grep -i -e '/img/epfl_small' -e '/latest/includes/epfl-header' -e 'id="nav-logo"' `            #récupère s'il y a un logo sur static.epfl.ch
if [ "$t1" != "" ]                                        #test s'il y a un logo sur un serveur centralisé
then
    echo -e "static: "$1", "$t1 >> dyna.log
    r=""
fi


#traitement des pages d'imprimantes
t1=`cat html.txt |grep -i -e 'HP Color LaserJet' -e 'hp LaserJet' -e 'hp/device' -e 'okiprintingsolutions' -e 'okilogo' `            #filtre
if [ "$t1" != "" ]                                        #test s'il y a un logo sur un serveur centralisé
then
    echo -e "printer: "$1 >> removed.log
    r=""
fi


#traitement des pages serveurs web vides et synology et cisco et netapp
t1=`cat html.txt |grep -i -e '<title>Apache2 ' -e 'alt="IIS7"' -e 'IIS Windows' -e 'iis-8' -e 'syno' -e 'cisco.com' -e 'data-netapp' `            #filtre
if [ "$t1" != "" ]                                        #test s'il y a un logo sur un serveur centralisé
then
    echo -e "srvweb1: "$1 >> removed.log
    r=""
fi








#traitement des pages serveurs tequila
if [ "`echo -e $r |grep -i 'tequila'`" != "" ]                                        #test si c'est une page tequila
then
    echo -e "tequila: "$1 >> removed.log
    r=""
fi

#traitement des pages serveurs archiveweb
if [ "`echo -e $r |grep -i 'archiveweb'`" != "" ]                                        #test si c'est une page archivée
then
    echo -e "archiveweb: "$1 >> removed.log
    r=""
fi

#2e traitement des pages serveurs archiveweb
curl --insecure --max-time 5 -Ivs $1  2>err.txt | sed "s/\r/\n/g" > header.txt                       #récupère le header HTTP
if [ "`cat header.txt |grep -i 'archiveweb'`" != "" ]                                        #test si c'est une page archivée
then
    echo -e "archiveweb: "$1 >> removed.log
    r=""
fi



echo $r


