#!/usr/bin/env bash
#Petit script pour parser tous la structure des sites web (./html) récupérée par le wget et de copier dans un dossier tous les fichiers images
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181101.1652

#source: 
#rappel: sshfs ubuntu@docker-zf1:/home/ubuntu /Users/zuzu/VirtualBox\ VM\ Masters/logomatch


echo ---------- copy_parse_images_files.sh

find html |grep -i -E 'gif|png|jpg|jpeg|svg' > liste_images.csv



echo -e "path" > tempzip.csv
head -n 1000 liste_images.csv >> tempzip.csv
read -p "enter"

rm -Rf ./images
mkdir images
cd images

INPUT=../tempzip.csv
OLDIFS=$IFS
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }

nblines=0
zsite="tmp"
while read path ; do
    echo $nblines
    if [ $nblines != "0" ] ; then
        echo -e "le fichier est: "$path
        file_name=`echo $path | sed "s/\//_/g"`
        echo -e "le file name est: "$file_name
        cp ../$path $file_name

#        site=`echo $site | awk -F "/" '{print $3}'`
#        echo -e "le site est: "$site
#        if [ "$zsite" != "$site" ] ; then
#            echo -e "on zip le dossier: "$zsite
#            zip -r ../$zsite".zip" .
#            echo -e "on remonte d'un étage"
#            cd ..
#            echo -e "on crée le nouveau dossier "$site" et on se déplace"
#            mkdir $site
#            cd $site
#            zsite=$site
#            echo -e "on aspire le nouveau site:"$site
#        fi
#        echo -e "on aspire: "$url
#        pwd
#        wget -O `echo $url | awk -F "/" '{ for(i=5 ; i <= NF ; i++) { printf "_%s",$i } printf "\n"}' | sed "s/\%20/_/g" | sed "s/\%2C//g"` $url
    fi
    ((nblines+=1))
    echo ""
done < $INPUT
IFS=$OLDIFS


#echo -e "on zip le dossier: "$zsite
#zip -r ../$zsite".zip" .






exit




find html |grep -i -E 'gif|png|jpg|jpeg|svg' |grep -i logo

echo -e "
il y a comme nombre de site scannés:"
wc ./data/urls_test.csv

echo -e "
il y a comme nombre de sites actifs:"
find ./html |grep '\.html' |wc

echo -e "
il y a comme nombre de fichiers image:"
find html |grep -i -E 'gif|png|jpg|jpeg|svg' |wc

echo -e "
il y a comme nombre de fichier avec le mot logo:"
find html |grep -i -E 'gif|png|jpg|jpeg|svg' |grep -i logo |wc





