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

MATCH_EXT="jpg"
SURE_MIN_MATCH_COUNT = 20
MAYBE_MATCH_COUNT = 5

class MImage():

  # class variables / constants
  sift = cv2.xfeatures2d.SIFT_create()

  def __init__(self, in_path):
    self.path = in_path
    img_rgb = cv2.imread(self.path)
    self.img = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
    self.kp, self.des = MImage.sift.detectAndCompute(self.img,None)
    self.name = os.path.splitext(os.path.basename(self.path))[0]

class Matcher():

  # class variables / constants
  DISTANCE_FACTOR = 0.7
  FLANN_INDEX_KDTREE = 1
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)

  def __init__(self, img2, img1):
    self.img1 = img1
    self.img2 = img2
    self.matches = Matcher.flann.knnMatch(img1.des,img2.des,k=2)
    self.score = 0
    for m,n in self.matches:
      if m.distance < Matcher.DISTANCE_FACTOR*n.distance:
        self.score = self.score + 1
    self.basepath=self.img2.name + "_" + self.img1.name + "." + MATCH_EXT

  def page(self):
    return self.img2

  def logo(self):
    return self.img1

  def save(self, match_path, show_max=20):
    good=[]
    for m,n in self.matches:
      if m.distance < Matcher.DISTANCE_FACTOR*n.distance:
        good.append(m)
    sgood = sorted(good, key = lambda x:x.distance)
    nshow = len(sgood) if show_max == 0 else show_max
    img3 = cv2.drawMatches(self.img1.img,self.img1.kp,self.img2.img,self.img2.kp,sgood[:nshow], None, flags=2)
    cv2.imwrite(match_path + self.basepath, img3)

# ----------------------------------------------------

# pages_file_or_dir=sys.argv[1]
# logos_file_or_dir=sys.argv[2]
# if (len(sys.argv))
# match_dir=sys.argv[3]

# print(match_dir)

pages_file_or_dir=sys.argv.pop(1)
logos_file_or_dir=sys.argv.pop(1)
if (len(sys.argv) > 1):
  match_dir=sys.argv.pop(1)
else:
  match_dir=None

if os.path.isdir(pages_file_or_dir):
  page_paths=glob.glob(pages_file_or_dir + "/*.png") + glob.glob(pages_file_or_dir + "/*.jpg")
else:
  page_paths=[pages_file_or_dir]


if os.path.isdir(logos_file_or_dir):
  logo_paths=glob.glob(logos_file_or_dir + "/*.png") + glob.glob(logos_file_or_dir + "/*.jpg")
else:
  logo_paths=[logos_file_or_dir]

logos=[]
for logo_path in logo_paths:
  logo = MImage(logo_path)
  logos.append(logo)

verbose=(len(page_paths)>1 or len(logos)>1)

for page_path in page_paths:
  page=MImage(page_path)

  print("\n"+page_path)

  max_score=0
  best_m=None
  for logo in logos:
    m=Matcher(page, logo)

    # print(page, logo, MIN_MATCH_COUNT, ypath)
    if (m.score > max_score): 
      max_score = m.score
      best_m = m

    print("%-20s %-20s %2d" % ("", logo.name, m.score))

    if match_dir is not None:
      m.save(match_dir + "/all/")

  ans=""
  if max_score < MAYBE_MATCH_COUNT:
    ans="no"
  else:
    if max_score > SURE_MIN_MATCH_COUNT:
      ans="yes"
    else:
      ans="maybe"
  if (verbose):
    print("%-20s %-20s %2d -> %s" % (page.name, best_m.logo().name, max_score, ans))
  else:
    print(max_score)

  if match_dir is not None:
    lpath="match/%s/%02d_%s.%3s" % (ans, max_score, page.name, MATCH_EXT)
    os.symlink("../all/"+best_m.basepath, lpath)
