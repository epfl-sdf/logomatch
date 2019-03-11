#!/bin/sh

awk '
  /CONT/{next;}
  {gsub("%", ""); gsub("--", "0"); print($7);}
' $1