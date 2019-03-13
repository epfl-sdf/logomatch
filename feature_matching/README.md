zf190313.1124

1) il faut builder le container Python OpenCV avec:<br>
cd docker<br>
docker build -t opencv .

pour tester le container:<br>
docker run -it -v $PWD:/wd -v $PWD/../test_pages/:/test_pages --entrypoint /bin/bash opencv


1.5) il faut créer un lien symbolique<br>


2) il faut faire tourner le script start.sh avec:<br>


rm -rf result2/ ; ./start.sh -p "docker run -v $PWD:/wd -v $PWD/../test_pages/:/test_pages opencv" ../test_pages/ result2

rm -rf work/ ; ./start.sh -p "docker run -v $PWD:/wd opencv" pages/2019-03-04/ work


rm -rf result2/ ; ./start.sh -p "docker run -v $PWD:/wd opencv" ../images.190301.0853/ result2



