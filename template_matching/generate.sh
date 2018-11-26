#!/bin/bash
#zf181126.1550

sizes="120 360"

nsizes=$(echo $sizes | wc -w)
nlogos=$(echo "$nsizes * 10" | bc -l)

for ext in png ; do
  [ -d logo/$ext ] || mkdir -p logo/$ext
done

which inkscape
haveis="$?"
if [ "$haveis" == "0" ] ; then
  echo "Inkscape is present and will be used to generate logos"
else
  echo "Inkscape is NOT present. Imagemagic's convert will be used to generate the logos"
fi

for svg in $(ls logo/*.svg) ; do 
  j=$(basename $svg .svg)
  for s in 120 360 ; do
    png=$(printf "logo/png/%s_%03d.png" $j $s)
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

for full in logo/png/c_*.png logo/png/ci_*.png logo/png/m_*.png logo/png/mi_*.png ; do
  crp=logo/png/cr1$(basename $full)
  if [ ! -f $crp ] ; then
    convert -gravity North -crop 54%x60% $full $crp
  fi
done

for full in logo/png/c_*.png logo/png/ci_*.png ; do
  crp=logo/png/cr2$(basename $full)
  if [ ! -f $crp ] ; then
    convert -gravity South -crop 100%x38% $full $crp
  fi
done

nl=$(ls -1 logo/png/*.png | wc  -l)
echo "nl=$nl   nlogos=$nlogos"
if [ $nl -gt $nlogos ] ; then
  echo "Unexpected number of logos. Regenerating from scratch"
  rm ./logo/png/*.png
  $0
fi

# for png in logo/png/*.png ; do
#   jpg=logo/jpg/$(basename $png .png).jpg
#   if [ ! -f $jpg ] ; then
#     convert $png $jpg
#   fi
# done

# [ -d pages ] || mkdir pages
# for s in 120 180 240 ; do
#   jpg=logo/c_$s.jpg
#   png=logo/c_$s.png
#   jpag=pages/logo_$s.jpg
#   ppag=pages/logo_$s.png
#   if [ ! -f $ppag ] ; then
#     convert -size 1024x1024 xc:white $png -gravity center -composite $ppag 
#   fi
#   if [ ! -f $jpag ] ; then
#     convert -size 1024x1024 xc:white $jpg -gravity center -composite $jpag 
#   fi
# done

# for ppag in pages/*.png ; do 
#   jpag=pages/$(basename $ppag .png).jpg
#   if [ ! -f $jpag ] ; then
#     convert $ppag $jpag
#   fi
# done

# for jpag in pages/*.jpg ; do 
#   ppag=pages/$(basename $jpag .jpg).png
#   if [ ! -f $ppag ] ; then
#     convert $jpag $ppag
#   fi
# done
