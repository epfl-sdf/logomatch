#!/usr/bin/env bash
#petit script pour faire faire une copie des images de résultat sur la clef USB 
#zf190312.1420

#source: 

#rsync -n -r -v -t --progress --stats ./images2/* zuzu@siipc6.epfl.ch:/Volumes/logomatch/181122.1400
#rsync -n -r -v -t --progress --stats ./images2/* zuzu@siipc6.epfl.ch:/Volumes/logomatch/181122.1400
rsync -n -r -v -t --progress --stats ~/logomatch/images.190301.0853/* zuzu@siipc6.epfl.ch:/Volumes/LOGOMATCH/180103.0928/images
rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/result/* zuzu@siipc6.epfl.ch:/Volumes/LOGOMATCH/180103.0928/result
rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/result/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/result"
rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images.190301.0853/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/images"


