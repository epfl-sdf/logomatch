#!/bin/sh

sh generate.sh

[ -d match ] || mkdir match
for d in all yes no maybe ; do
  if [ -d match/$d ] ; then
    rm match/$d/*
  else
    mkdir match/$d
  fi
done

# docker run -it -v $PWD:/app -w=/app valian/docker-python-opencv-ffmpeg
# pyenv activate opencv
python test3.py

