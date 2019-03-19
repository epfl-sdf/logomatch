zf190319.1108

1) il faut builder le container Python OpenCV avec:<br>
cd docker ; docker build -t opencv . ; cd ..

pour tester le container:<br>

export zpages="images" ; docker run -it -u $(id -u ${USER}):$(id -g ${USER}) -v $PWD:/wd -v $PWD/../../../logomatch/$zpages/:/wd/$zpages --entrypoint /bin/bash opencv


1.5) vérifier qu'on a bien le dossier des ./logos à chercher !<br>
s'il n'y a pas faire tourner:

./generate_logos.sh


2) il faut faire tourner le script start.sh avec:<br>

#sudo rm -rf result2/ ; export zpages="test_pages" ; ./start.sh -p "docker run -v $PWD:/wd -v $PWD/../$zpages/:/$zpages opencv" ../$zpages/ result2

#sudo rm -rf result2/ ; export zpages="images.190301.0853" ; ./start.sh -p "docker run -v $PWD:/wd -v $PWD/../$zpages/:/$zpages opencv" ../$zpages/ result2

rm -rf result2/ ; export zpages="images" ; ./start.sh -p "docker run -u $(id -u ${USER}):$(id -g ${USER}) -v $PWD:/wd -v $PWD/../../../logomatch/$zpages/:/wd/$zpages opencv" $zpages/ result2




