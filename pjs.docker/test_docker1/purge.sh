#!/bin/bash
#Petit script pour nettoyer tout le binz
#zf181211.1144

docker container rm -f -v phantomjs_z1
docker image rm -f phantomjs_z:001

./list.sh


