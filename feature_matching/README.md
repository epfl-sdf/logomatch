zf190313.1405

1) il faut builder le container Python OpenCV avec:<br>
cd docker ; docker build -t opencv . ; cd ..

pour tester le container:<br>
docker run -it -v $PWD:/wd -v $PWD/../test_pages/:/test_pages --entrypoint /bin/bash opencv


2) il faut faire tourner le script start.sh avec:<br>

sudo rm -rf result2/ ; export zpages="test_pages" ; ./start.sh -p "docker run -v $PWD:/wd -v $PWD/../$zpages/:/$zpages opencv" ../$zpages/ result2

sudo rm -rf result2/ ; export zpages="images.190301.0853" ; ./start.sh -p "docker run -v $PWD:/wd -v $PWD/../$zpages/:/$zpages opencv" ../$zpages/ result2



