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
import argparse

MATCH_EXT="jpg"
DEFAULT_YES_ABOVE = 16
DEFAULT_NO_BELOW  = 8
DEFAULT_MATCHES_TO_DRAW = 50

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
  MIN_MATCH_COUNT = 4
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)

  def __init__(self, img2, img1):
    self.img1 = img1
    self.img2 = img2

    matches = Matcher.flann.knnMatch(img1.des,img2.des,k=2)
    lowe_matches=[]
    for m,n in matches:
      if m.distance < Matcher.DISTANCE_FACTOR*n.distance:
        lowe_matches.append(m)

    # If enough points, a second selection is done by the Homography algorithm that keeps
    # only the points that can be linked geometrically
    if len(lowe_matches) > Matcher.MIN_MATCH_COUNT:
      src_pts = np.float32([ self.img1.kp[m.queryIdx].pt for m in lowe_matches ]).reshape(-1,1,2)
      dst_pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in lowe_matches ]).reshape(-1,1,2)
      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      select_mask = mask.ravel().tolist()
      self.good_matches = []
      for i, m in enumerate(select_mask):
        if (m==1):
          self.good_matches.append(lowe_matches[i])
    else:
      self.good_matches = lowe_matches

    self.score = len(self.good_matches)
    self.basepath="%02d_%s_%s.%s" % (self.score, self.img2.name, self.img1.name, MATCH_EXT)

    # points=[]
    # for m in self.good_matches[:3]:
    #   p=[img2.kp[m.trainIdx].pt[0], img2.kp[m.trainIdx].pt[1]]
    #   points.append(p)
    # self.ave = np.mean(points, 0)
    # self.std = np.std(points, 0)
    # print("ave = %6.2f  %6.2f" % (self.ave[0], self.ave[1]) )
    # print("std = %6.2f  %6.2f" % (self.std[0], self.std[1]) )

    # sgood = sorted(self.good_matches, key = lambda x:x.distance)
    # for m in sgood:
    #   # print("distance: %6.2f - %6.2f" % (m.distance, n.distance) )
    #   print("\npage: %d = %6.2f %6.2f" % (m.trainIdx, img2.kp[m.trainIdx].pt[0], img2.kp[m.trainIdx].pt[1]) )
    #   print("logo: %d = %6.2f %6.2f" % (m.queryIdx, img1.kp[m.queryIdx].pt[0], img1.kp[m.queryIdx].pt[1]) )

  def page(self):
    return self.img2

  def logo(self):
    return self.img1

  def save(self, match_path, show_max=DEFAULT_MATCHES_TO_DRAW):
    good=[]
    sgood = sorted(self.good_matches, key = lambda x:x.distance)
    nshow = len(sgood) if show_max == 0 else show_max
    img3 = cv2.drawMatches(self.img1.img,self.img1.kp,self.img2.img,self.img2.kp,sgood[:nshow], None, flags=2)

    # # c=self.ave + (self.img1.img.shape[1], 0)
    # c=(float(self.ave[0])+100,100)
    # # print(self.ave[0])
    # a=(100, 50)
    # cv2.ellipse(img3,c,a,0,0,360,255,3)

    cv2.imwrite(match_path + self.basepath, img3)

# ----------------------------------------------------

parser = argparse.ArgumentParser(
  prog = "logospotter",
  description = "Logo spotter",
  epilog = """ This program scans one or more images ('page'), for presence of another image ('logo').
               If a folder of 'pages' is provided, it will scann all of them;
               If a folder of 'logos' is provided, it will search for the best match.
           """
)
parser.add_argument("-v", "--verbose", action='store_true', help="Increase output level")
parser.add_argument("-n", "--no_below", action='store', type=int, default=DEFAULT_NO_BELOW, help="Below this threshold, images do not match")
parser.add_argument("-y", "--yes_above", action='store', type=int, default=DEFAULT_YES_ABOVE, help="Below this threshold, images do not match")
parser.add_argument("-s", "--show_upto", action='store', type=int, default=DEFAULT_MATCHES_TO_DRAW, help="Number of matches to show in the inspection image")
parser.add_argument("-m", "--matchdir", action='store', help="Output directory for match images (mostly used for inspecting output while debugging)")
parser.add_argument("page", help="A file or a folder with 'page' images")
parser.add_argument("logo", help="A file or a folder with 'logo' images")
opts = parser.parse_args()

# validate match dir and evetually create the various folder that are needed
if opts.matchdir is not None:
  for d in [opts.matchdir, opts.matchdir+"/all", opts.matchdir+"/yes", opts.matchdir+"/no", opts.matchdir+"/maybe"]:
    if (not os.path.exists(d)):
      os.mkdir(d)
    elif (not (os.path.isdir(d) and os.access(d, os.W_OK))):
      raise("Folder " + d + " is not a directory or is not writable")

if os.path.isdir(opts.page):
  page_paths=glob.glob(opts.page + "/*.png") + glob.glob(opts.page + "/*.jpg")
else:
  page_paths=[opts.page]

if os.path.isdir(opts.logo):
  logo_paths=glob.glob(opts.logo + "/*.png") + glob.glob(opts.logo + "/*.jpg")
else:
  logo_paths=[opts.logo]

many_pages = (len(page_paths)>1)
many_logos = (len(logo_paths)>1)
verbose=(many_pages or many_logos)

logos=[]
for logo_path in logo_paths:
  logo = MImage(logo_path)
  logos.append(logo)


for page_path in page_paths:
  page=MImage(page_path)

  if (many_pages and opts.verbose): print("\n"+page_path)

  max_score=0
  best_m=None
  for logo in logos:
    m=Matcher(page, logo)

    # print(page, logo, MIN_MATCH_COUNT, ypath)
    if (m.score > max_score): 
      max_score = m.score
      best_m = m

    if (many_logos and opts.verbose): print("%-20s %-20s %2d" % ("", logo.name, m.score))

    if opts.matchdir is not None:
      m.save(opts.matchdir + "/all/", opts.show_upto)

  ans=""
  if max_score < opts.no_below:
    ans="no"
  else:
    if max_score > opts.yes_above:
      ans="yes"
    else:
      ans="maybe"
  if (verbose):
    print("%-20s %-20s %2d -> %s" % (page.name, best_m.logo().name, max_score, ans))
  else:
    print(max_score)

  if opts.matchdir is not None:
    lpath="match/" + ans + "/" + best_m.basepath
    os.symlink("../all/"+best_m.basepath, lpath)
