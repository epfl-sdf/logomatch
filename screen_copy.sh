#!/usr/bin/env bash
#petit script pour faire une copie d'écran de la homes pages d'un sites web
#zf181122.1053

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/


phantomjs phantomjs_screen_copy.js $1 $2                #>/dev/null
