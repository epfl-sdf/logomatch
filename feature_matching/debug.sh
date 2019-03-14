#!/bin/sh
# rm -rf debug/m1
# rm -rf debug/m2
# # docker run --security-opt=seccomp=unconfined -v /Users/cangiani/iDevProjects/logomatch/feature_matching:/wd opencv feature_matcher.py -v -K 5 -l 0.68 -n 4 -y 10 -m debug/m1 ./debug/pages logos
# docker run --security-opt=seccomp=unconfined -v /Users/cangiani/iDevProjects/logomatch/feature_matching:/wd opencv feature_matcher.py -v -K 5 -l 0.68 -n 4 -y 10 -m debug/m2 ./pages/2019-03-04 logos
# res=$?
# echo "res = $res"


[ -d debug ] && rm -rf debug
docker run -v /Users/cangiani/iDevProjects/logomatch/feature_matching:/wd opencv feature_matcher2.py \
        -R 2000 -v -K 5 -l 0.95 -n 4 -y 10 -p 4000 -ph 600 -ps 400 \
        -m debug pages/debug logos
