#!/usr/bin/env bash
#petit script pour faire faire une copie des images de résultat sur la clef USB 
#zf190528.1546

ATTENTION, il faut enlever le '-n' !

#rsync -n -r -v -t --progress --stats ./images2/* zuzu@siipc6.epfl.ch:/Volumes/logomatch/181122.1400
#rsync -n -r -v -t --progress --stats ./images2/* zuzu@siipc6.epfl.ch:/Volumes/logomatch/181122.1400
rsync -n -r -v -t --progress --stats ~/logomatch/images.190301.0853/* zuzu@siipc6.epfl.ch:/Volumes/LOGOMATCH/180103.0928/images
rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/result/* zuzu@siipc6.epfl.ch:/Volumes/LOGOMATCH/180103.0928/result
rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/result/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/result"
rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images.190301.0853/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/images"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images.190319.1100/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190319/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190319/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190325/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190325/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190401/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190401/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190408/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190408/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190415/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190415/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190425/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190425/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190502/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190502/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190509/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190509/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190515/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190515/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190523/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190523/result"

rsync -n -r -v -t --progress --stats /home/zuzu/logomatch/images/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190528/images"
rsync -n -r -v -t --progress --stats /home/zuzu/giova/logomatch/feature_matching/result2/* zuzu@siipc6.epfl.ch:"/Users/zuzu/VirtualBox\ VM\ Masters/No\ zlightbackup/logomatch/190528/result"


