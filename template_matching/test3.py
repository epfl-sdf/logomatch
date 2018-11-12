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
import cv2 as cv
# from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 3
SHOW_MATCHES = 20

def match(img2_path, img1_path, thr, match_path=None):

  img1 = cv.imread(img1_path) # queryImage
  img2 = cv.imread(img2_path) # trainImage

  # Trasform to Grayscale
  img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
  img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

  # Initiate SIFT detector
  sift = cv.xfeatures2d.SIFT_create()

  # find the keypoints and descriptors with SIFT
  kp1, des1 = sift.detectAndCompute(img1,None)
  kp2, des2 = sift.detectAndCompute(img2,None)

  FLANN_INDEX_KDTREE = 1
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)

  flann = cv.FlannBasedMatcher(index_params, search_params)

  matches = flann.knnMatch(des1,des2,k=2)

  good = []
  for m,n in matches:
    if m.distance < 0.7*n.distance:
      good.append(m)

  if match_path is not Null:
    matches = sorted(good, key = lambda x:x[0].distance)
    img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good[:SHOW_MATCHES], None, flags=2)
    cv.imwrite(match_path, img3)

  return len(good)

  # plt.imshow(img3, 'gray'),plt.show()

# ----------------------------------------------------

pages=glob.glob("pages/jpg/*.jpg")
logos=glob.glob("logo/jpg/*.jpg")

print(pages)
print(logos)

for page in pages:
  pname=os.path.splitext(os.path.basename(page))[0]
  m_max=0
  print("\n"+page)
  for logo in logos:
    lname=os.path.splitext(os.path.basename(logo))[0]
    mpath=pname + "_" + lname + ".jpg"
    m=match(page, logo, MIN_MATCH_COUNT, "match/all/"+mpath)
    if (m>m_max): 
      m_max = m
    print("%-40s %-40s %2d / %2d" % (pname, lname, m, MIN_MATCH_COUNT))

  if m_max < MIN_MATCH_COUNT:
    npath="match/no/%02d_%s.jpg" % (m_max, pname)
    os.symlink("../all/"+mpath, npath)
  else:
    ypath="match/yes/%02d_%s.jpg" % (m_max, pname)
    os.symlink("../all/"+mpath, ypath)
