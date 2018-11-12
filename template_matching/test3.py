# Run with
# rm match/no/*
# rm match/yes/*
# docker run -it -v $PWD:/app -w=/app valian/docker-python-opencv-ffmpeg python test3.py
#
#zf181112.1617

import os.path
import glob
import sys
import numpy as np
import cv2

SURE_MIN_MATCH_COUNT = 12
MAYBE_MATCH_COUNT = 5
DISTANCE_FACTOR = 0.7

# Ho many features to show in the match_patch image
SHOW_MATCHES = 20

def match(img2_path, img1_path, match_path=None):
  img1_rgb = cv2.imread(img1_path) # queryImage
  img2_rgb = cv2.imread(img2_path) # trainImage
  img1 = cv2.cvtColor(img1_rgb,cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2_rgb,cv2.COLOR_BGR2GRAY)

  # Initiate SIFT detector
  sift = cv2.xfeatures2d.SIFT_create()

  # find the keypoints and descriptors with SIFT
  kp1, des1 = sift.detectAndCompute(img1,None)
  kp2, des2 = sift.detectAndCompute(img2,None)

  FLANN_INDEX_KDTREE = 1
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)

  flann = cv2.FlannBasedMatcher(index_params, search_params)

  matches = flann.knnMatch(des1,des2,k=2)

  good = []
  ngood = 0
  for m,n in matches:
    if m.distance < DISTANCE_FACTOR*n.distance:
      ngood = ngood + 1
      good.append(m)

  if match_path is not None:
    matches = sorted(good, key = lambda x:x.distance)
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:SHOW_MATCHES], None, flags=2)
    cv2.imwrite(match_path, img3)

  return ngood

# ----------------------------------------------------

pages=glob.glob("pages/jpg/*.jpg")
logos=glob.glob("logo/jpg/*.jpg")

for page in pages:
  pname=os.path.splitext(os.path.basename(page))[0]
  m_max=0
  m_path=""
  m_logo=""
  print("\n"+page)
  for logo in logos:
    lname=os.path.splitext(os.path.basename(logo))[0]
    mpath=pname + "_" + lname + ".jpg"
    m=match(page, logo, "match/all/"+mpath)
    # m=match5(page, logo)
    if (m>m_max): 
      m_max = m
      m_logo = lname
      m_path = mpath
    print("%-20s %-20s %2d" % ("", lname, m))

  ans=""
  if m_max < MAYBE_MATCH_COUNT:
    ans="no"
  else:
    if m_max > SURE_MIN_MATCH_COUNT:
      ans="yes"
    else:
      ans="maybe"

  print("%-20s %-20s %2d -> %s" % (pname, m_logo, m_max, ans))
  lpath="match/%s/%02d_%s.jpg" % (ans, m_max, pname)
  os.symlink("../all/"+m_path, lpath)
