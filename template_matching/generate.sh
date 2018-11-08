#!/bin/bash

for ext in png jpg ; do
  [ -d logo/$ext ] || mkdir -p logo/$ext
done

for svg in $(ls logo/*.svg) ; do 
  j=$(basename $svg .svg)
  for i in {20..140}; do 
    let s=2*$i
    png=logo/png/$(printf "%s_%03d.png" $j $s)
    if [ ! -f $png ] ; then
      # convert -density $s $svg $png 
      # inkscape -z $svg  --export-dpi=$s --export-png=$png
      inkscape -z $PWD/$svg  --export-width=$s --export-png=$PWD/$png
    fi
  done
done

for full in logo/png/c_*.png ; do
  crp=logo/png/cr$(basename $full)
  if [ ! -f $crp ] ; then
    # convert -crop 54%x59%+35%+0 $full $crp
    convert -gravity North -crop 54%x59% $full $crp
  fi
done

for png in logo/png/*.png ; do
  jpg=logo/jpg/$(basename $png .png).jpg
  if [ ! -f $jpg ] ; then
    convert $png $jpg
  fi
done

[ -d pages ] || mkdir pages
for s in 100 140 200 ; do
  jpg=logo/jpg/c_$s.jpg
  png=logo/png/c_$s.png
  jpag=pages/logo_$s.jpg
  ppag=pages/logo_$s.png
  if [ ! -f $ppag ] ; then
    convert -size 1024x1024 xc:white $png -gravity center -composite $ppag 
  fi
  if [ ! -f $jpag ] ; then
    convert -size 1024x1024 xc:white $jpg -gravity center -composite $jpag 
  fi
done

for ppag in pages/*.png ; do 
  jpag=pages/$(basename $ppag .png).jpg
  if [ ! -f $jpag ] ; then
    convert $ppag $jpag
  fi
done

for jpag in pages/*.jpg ; do 
  ppag=pages/$(basename $jpag .jpg).png
  if [ ! -f $ppag ] ; then
    convert $jpag $ppag
  fi
done

[ -d pages/gray ] || mkdir -p pages/gray
for rgb in pages/*.jpg ; do
  gra=pages/gray/$(basename $rgb)
  convert $rgb -fx '(r+g+b)/3' -colorspace Gray $gra
done

[ -d logo/gray ] || mkdir -p logo/gray
for l in c_280.jpg ci_280.jpg crc_280.jpg ; do
  rgb=logo/jpg/$l
  gra=logo/gray/$l
  convert $rgb -fx '(r+g+b)/3' -colorspace Gray $gra
done



