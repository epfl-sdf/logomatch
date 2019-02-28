#!/usr/bin/env bash
#petit script pour faire le preprocessing d'un site web 
#afin d'épurer les sites à scanner par la suite
#zf181121.1410

#source: https://www.cyberciti.biz/faq/unix-linux-bash-read-comma-separated-cvsfile/

url=$1

url=`./loop_url_process_header.sh $url`                 #test les redirections et les erreurs dans le header

if [ "$url" != "" ]
then
    url=`./url_process_html.sh $url`                    #test les redirections dans le html
fi

if [ "$url" != "" ]
then
#    echo -e "url: "$url
    echo $url
fi

