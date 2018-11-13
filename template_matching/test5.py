# Run with
# rm match/no/*
# rm match/yes/*
# docker run -it -v $PWD:/app -w=/app valian/docker-python-opencv-ffmpeg python test3.py
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html
import os.path
import glob
import sys
import numpy as np
import cv2

DISTANCE_FACTOR = 0.7

def match(img2_path, img1_path):
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

  ngood = 0
  for m,n in matches:
    if m.distance < DISTANCE_FACTOR*n.distance:
      ngood = ngood + 1

  return ngood

# ----------------------------------------------------

pages_file_or_dir=sys.argv[1]
logos_file_or_dir=sys.argv[2]

if os.path.isdir(pages_file_or_dir):
  pages=glob.glob(pages_file_or_dir + "/*.png")
else:
  pages=[pages_file_or_dir]

if os.path.isdir(logos_file_or_dir):
  logos=glob.glob(logos_file_or_dir + "/*.jpg")
else:
  logos=[logos_file_or_dir]

verbose=(len(pages)>1 or len(logos)>1)

for page in pages:
  pname=os.path.splitext(os.path.basename(page))[0]
  m_max=0
  m_logo=""
  for logo in logos:
    lname=os.path.splitext(os.path.basename(logo))[0]

    # print(page, logo, MIN_MATCH_COUNT, ypath)
    m=match(page, logo)
    if (m>m_max): 
      m_max = m
      m_logo = lname

  if (verbose):
    print("%-20s %-20s %2d" % (pname, m_logo, m_max))
  else:
    print(m_max)
