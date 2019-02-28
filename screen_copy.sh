#!/usr/bin/env bash
#petit script pour faire une copie d'écran de la homes pages d'un sites web
#zf190228.1909

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/


#phantomjs --ignore-ssl-errors=true phantomjs_screen_copy.js $1 $2                #>/dev/null
timeout 10 firefox --screenshot $2 $1                #>/dev/null

