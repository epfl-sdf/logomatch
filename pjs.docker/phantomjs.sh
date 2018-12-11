#!/bin/bash
#Petit script pour démarrer le binz
#zf181210.1105
# source: 


#test si l'argument est vide
if [ -z "$1" ]
  then
    echo -e "\nSyntax: ./start.sh site_name user passwd \n\n"
    exit
fi




docker build -t pjs ./pjs.docker
docker run -v $(pwd):/wd pjs phantomjs_script.js



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
