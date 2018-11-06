#!/usr/bin/env bash
#Petit script pour parser tous la structure des sites web (./html) récupérée par le wget et de copier dans un dossier tous les fichiers images
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181106.1645

#source: 
#rappel: sshfs ubuntu@docker-zf1:/home/ubuntu /Users/zuzu/VirtualBox\ VM\ Masters/logomatch

echo ---------- copy_parse_images_files.sh
read -p "enter"

echo -e "name" > liste_images_name.csv

echo -e "path" > liste_images_path.csv
find html |grep -i -E 'gif|png|jpg|jpeg|svg' >> liste_images_path.csv
head -n 100000 liste_images_path.csv > tmp.csv

rm -Rf ./images
mkdir images
cd images

INPUT=../tmp.csv
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
        echo -e $file_name >> ../liste_images_name.csv
        cp ../$path $file_name
    fi
    ((nblines+=1))
    echo ""
done < $INPUT
IFS=$OLDIFS



