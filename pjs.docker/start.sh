#!/bin/bash
#Petit script pour builder le binz
#zf181210.1112
# source: 

docker build -t pjs .
echo -e "\npress [ENTER]" ; read p

docker image ls
echo -e "\npress [ENTER]" ; read p

echo -e "

Il faut utiliser après:

./pjs.sh script_phantomjs_a_tourner.js

"


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
