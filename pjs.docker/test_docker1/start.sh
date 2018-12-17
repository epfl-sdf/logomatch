#!/bin/bash
#Petit script pour builder le binz
#zf181211.1145
# source: 



docker build -t phantomjs_z:001 .
echo -e "\npress [ENTER]" ; read p

docker image ls
echo -e "\npress [ENTER]" ; read p

docker run -d -i --name="phantomjs_z1" phantomjs_z:001
echo -e "press [ENTER]" ; read p

docker container ls
echo -e "press [ENTER]" ; read p

docker exec -ti phantomjs_z1 /bin/bash

