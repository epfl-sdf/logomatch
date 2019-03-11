#!/bin/sh

wd=$1
[ -n "$wd" ] || echo "Prease provide a work directory"
[ -d $wd ] || echo "Prease provide a work directory"

for d in $wd/m[123456789] ; do
  [ -d $d ] || exit 0

  pushd $d
  for ext in yes no maybe ; do
    if [ -d $ext ] ; then
      odir=${ext}_files
      mkdir $odir
      for f in $ext/*.jpg ; do 
        cp $f $odir/
      done
      echo rm -rf $ext/ && mv $odir $ext
    fi 
  done
  popd
done
