#!/bin/sh


[ -d pnglogo ] || mkdir pnglogo
# for page in pages/*.png ; do
for page in pages/is_100.png; do
  for logo in pnglogo/*.png ; do 
    python test1.py $page $logo
  done
done
