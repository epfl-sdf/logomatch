#!/bin/bash

[ -d pnglogo ] || mkdir pnglogo
for svg in $(ls logo/*.svg) ; do 
  j=$(basename $svg .svg)
  for i in {20..140}; do 
    let s=2*$i
    png=pnglogo/$(printf "%s_%03d.png" $j $s)
    echo "$j $i   $s   $ss"
    if [ ! -f $png ] ; then
      # convert -density $s $svg $png 
      # inkscape -z $svg  --export-dpi=$s --export-png=$png
      inkscape -z $PWD/$svg  --export-width=$s --export-png=$PWD/$png
    fi
  done
done

[ -d pages ] || mkdir pages
for s in 100 140 ; do
  png=pnglogo/c_$s.png
  pag=pages/is_$s.png
  if [ ! -f $pag ] ; then
    convert -size 1024x1024 xc:white $png -gravity center -composite $pag 
  fi
done