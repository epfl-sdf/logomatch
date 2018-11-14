#!/usr/bin/env bash

shopt -s extglob

t1="toto URL= tutu"
t1='<meta http-equiv="refresh" content="1; URL=/web/guest/fr/websys/webArch/message.cgi?messageID=MSG_JAVASCRIPTOFF&buttonURL=/../../../">'



#tmp=${t1#*[uU][rR][lL]=}   # remove prefix ending in "url="


tmp=${t1#*+(url|URL)=}   # remove prefix ending in "url="


#tmp=${t1//#*url=/toto}   # remove prefix ending in "url="


#tmp2=${tmp#*URL=}   # remove prefix ending in "url="

echo $tmp

