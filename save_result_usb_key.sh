#!/usr/bin/env bash
#petit script pour faire faire une copie des images de résultat sur la clef USB 
#zf181122.1644

#source: 

#rsync -n -r -v -t --progress --stats ./images2/* zuzu@siipc6.epfl.ch:/Volumes/logomatch/181122.1400
rsync -n -r -v -t --progress --stats ./images2/* zuzu@siipc6.epfl.ch:/Volumes/logomatch/181122.1400

