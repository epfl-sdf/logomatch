#!/usr/bin/env bash
#Petit script pour installer tout ce qu'il faut pour logomatch
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181113.1123

#source: https://pypi.org/project/opencv-contrib-python/
#et la fin de ceci: http://answers.opencv.org/question/199318/how-to-use-sift-in-python/


#pour PhantomJS
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt update
sudo apt install -y nodejs build-essential phantomjs
#node -v
#npm -v
#npm install phantomjs --save

#pour OpenCV
sudo apt update
sudo apt install -y python-pip python-tk pinta
sudo -H python -m pip install -U pip
sudo -H python -m pip install -U matplotlib
sudo -H pip install opencv-contrib-python==3.4.2.17
