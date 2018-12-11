#!/bin/bash
#Petit script pour démarrer le binz
#zf181210.1119
# source: 


#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./pjs.sh script_phantomjs_a_tourner.js \n\n"
    exit
fi

docker run -d -i -v $(pwd):/wd --name="pjs1" pjs
docker exec -ti pjs1 /bin/sh


exit



 $1 $2 $3 $4



exit


docker build -t phantomjs:001 .
echo -e "\npress [ENTER]" ; read p

docker image ls
echo -e "\npress [ENTER]" ; read p

docker run -d -i --name="phantomjs1" phantomjs:001
echo -e "press [ENTER]" ; read p

docker container ls
echo -e "press [ENTER]" ; read p

docker exec -ti phantomjs1 /bin/sh
