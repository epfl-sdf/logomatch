#!/usr/bin/env bash

shopt -s extglob




        str=$1
        echo "${str: -1}"
        if [ "${str: -1}" = "/" ] || [ "${str: -1}" = "?" ]                                 #test si c'est une url relative ou absolue
        then
            echo -e "toto"
        fi


