#!/usr/bin/env bash
#petit script pour faire faire une copie des images sur un autre serveur pour des tests
#zf181122.1109

#source: 

#rsync -n --delete -r -v -t --progress --stats ./images/* ubuntu@128.178.116.112:/home/ubuntu/screen_copy_images
rsync -r -v -t --progress --stats ./images/* ubuntu@128.178.116.112:/home/ubuntu/screen_copy_images

