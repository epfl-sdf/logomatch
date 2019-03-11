#!/bin/sh
rm -rf debug/m1
rm -rf debug/m2
# docker run --security-opt=seccomp=unconfined -v /Users/cangiani/iDevProjects/logomatch/feature_matching:/wd opencv feature_matcher.py -v -K 5 -l 0.68 -n 4 -y 10 -m debug/m1 ./debug/pages logos
docker run --security-opt=seccomp=unconfined -v /Users/cangiani/iDevProjects/logomatch/feature_matching:/wd opencv feature_matcher.py -v -K 5 -l 0.68 -n 4 -y 10 -m debug/m2 ./pages/2019-03-04 logos
res=$?
echo "res = $res"
