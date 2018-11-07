#!/usr/bin/env bash
#Petit script pour installer tout ce qu'il faut pour PhantomJS
#ATTENTION: ça été fait pour une structure perso !
#faudra modifier le script pour d'autres structures
#zf181107.1653

#source: 

curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt update
sudo apt install -y nodejs build-essential phantomjs
node -v
npm -v
#npm install phantomjs --save



exit

