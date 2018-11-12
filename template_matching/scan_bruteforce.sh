#!/bin/sh

# for ext in jpg png ; do
#   for page in pages/*.$ext ; do
#     # for logo in logo/$ext/c_*.$ext logo/$ext/ci_*.$ext ; do 
#     for logo in logo/$ext/c_*.$ext logo/$ext/crc_*.$ext ; do 
#       grep -q "$page $logo" out || (python test2.py $page $logo | tee -a out)
#     done
#   done
# done

python -c '
import re
print("%-40s %-40s %8s %8s %8s" % ("page name", "best match logo", "min dist", "avg. dist", "min/avg"))
s={};
with open("out") as f:
  lines = f.readlines()

for ll in lines:
  l=ll.strip()
  page,logo,minvs =l.split()[1:4]
  minv=float(minvs)
  k=page
  if (k not in s):
    a={
      "s": 0.0,
      "v": minv,
      "n": 0,
      "l": logo,
    }
  else:
    a=s[k]

  a["s"] = a["s"] + minv
  a["n"] = a["n"] + 1
  if (minv < a["v"]):
    a["v"] = minv
    a["l"] = logo

  s[k]=a

for page in s :
  a=s[page]
  av=a["s"]/a["n"]
  print("%-40s %-40s %8.5f %8.5f %8.5f" % (page, a["l"], a["v"], av, a["v"]/av))
'
