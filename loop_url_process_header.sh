#!/usr/bin/env bash
#Petit script pour chercher les redirections récursives dans les headers
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181121.11106

#source:  https://stackoverflow.com/questions/428109/extract-substring-in-bash
#note:

shopt -s extglob                                                        #demande au bash de supporter les pipes !

url=$1
url1=`./url_process_header.sh $url`
nbloop=0

while [ "$url" != "$url1" ]; do
#    echo -e "url: "$url
    url=$url1
    url1=`./url_process_header.sh $url`
    ((nbloop+=1))
    if [ $nbloop -eq 10 ]                                               #test si cela boucle
    then
        url=$url1                                                       #sort de la boucle
    fi
done
#echo -e "url1: "$url1"\n"

echo -e $url1

