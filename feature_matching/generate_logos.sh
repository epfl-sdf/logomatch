#!/bin/bash
#zf181126.1550

sizes="120 360"

nsizes=$(echo $sizes | wc -w)
nlogos=$(echo "$nsizes * 10" | bc -l)

if [ -z "$1" ] ; then
  ldir="logos"
else
  ldir=$1
fi

[ -d $ldir ] || mkdir $ldir

which inkscape
haveis="$?"
if [ "$haveis" == "0" ] ; then
  echo "Inkscape is present and will be used to generate logos"
else
  echo "Inkscape is NOT present. Imagemagic's convert will be used to generate the logos"
fi

for svg in $(ls ../logos/*.svg) ; do 
  j=$(basename $svg .svg)
  for s in 120 360 ; do
    png=$(printf "$ldir/%s_%03d.png" $j $s)
    if [ ! -f $png ] ; then
      if [ "$haveis" == "0" ] ; then
        inkscape -z $PWD/$svg  --export-width=$s --export-png=$PWD/$png
      else
        d=$(echo "$s*210.528/96" | bc -l) # in svg file size i 210 and density is 96 
        convert -density $d $svg $png
      fi
    fi
  done
done

for full in $ldir/c_*.png $ldir/ci_*.png $ldir/m_*.png $ldir/mi_*.png ; do
  crp=$ldir/cr1$(basename $full)
  if [ ! -f $crp ] ; then
    convert -gravity North -crop 54%x60% $full $crp
  fi
done

for full in $ldir/c_*.png $ldir/ci_*.png ; do
  crp=$ldir/cr2$(basename $full)
  if [ ! -f $crp ] ; then
    convert -gravity South -crop 100%x38% $full $crp
  fi
done

nl=$(ls -1 $ldir/*.png | wc  -l)
if [ $nl -gt $nlogos ] ; then
  echo "Unexpected number of logos. Regenerating from scratch"
  rm ./$ldir/*.png
  $0
fi