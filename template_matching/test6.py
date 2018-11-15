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
  LOWE_FACTOR = 0.7
  GIOVA_FACTOR = 0.9
  GIOVA_THRESHOLD = 0
  FLANN_INDEX_KDTREE = 1
  MIN_MATCH_COUNT = 4

  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)

  def __init__(self, img2, img1):
    self.img1 = img1
    self.img2 = img2
    self.good_matches = None
    try:
      self.matches = Matcher.flann.knnMatch(self.img1.des,self.img2.des,k=2)
    except:
      self.matches=None
      self.good_matches=[]

  def match(self, 
            lowe_factor  = 0.7,
            giova_factor = 0.9,
            giova_thr    = 0,
          ):

    if self.matches is None: return 0

    if (giova_thr > 0):
      dmin = min(self.matches, key=lambda v: v[0].distance)[0].distance
      dmax = max(self.matches, key=lambda v: v[0].distance)[0].distance
      giova_maxdist = dmin + giova_thr * (dmax - dmin)
    else:
      giova_maxdist = 0.0

    lowe_matches=[]
    for m,n in self.matches:
      if m.distance < lowe_factor*n.distance or (m.distance < giova_maxdist and m.distance < giova_factor*n.distance):
        lowe_matches.append(m)

    self.homographyFilter(lowe_matches)

    # self.score = len(self.good_matches)
    # self.basepath="%02d_%s_%s.%s" % (self.score(), self.img2.name, self.img1.name, MATCH_EXT)
    return self.score()

  # This just take the matches with smallest NN distance and let homography filter based on geometry
  def match_simpler(self, max_count=25):
    if self.matches is None: return 0
    small_dist_matches = []
    for m,n in sorted(self.matches, key=lambda v: v[0].distance)[:max_count]:
      small_dist_matches.append(m)
    self.homographyFilter(small_dist_matches)
    return self.score()

  def homographyFilter(self, matches):
    # If enough points, a second selection is done by the Homography algorithm that keeps
    # only the points that can be linked geometrically
    if len(matches) > Matcher.MIN_MATCH_COUNT:
      src_pts = np.float32([ self.img1.kp[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
      dst_pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      select_mask = mask.ravel().tolist()
      self.good_matches = []
      for i, m in enumerate(select_mask):
        if (m==1):
          self.good_matches.append(matches[i])
    else:
      self.good_matches = matches

  def score(self):
    if self.good_matches is None:
      return None
    else:
      return len(self.good_matches)

  def basepath(self):
    if self.good_matches is None:
      return ("%s_%s.%s" % (self.img2.name, self.img1.name, MATCH_EXT))
    else:
      return ("%02d_%s_%s.%s" % (self.score(), self.img2.name, self.img1.name, MATCH_EXT))


  def page(self):
    return self.img2

  def logo(self):
    return self.img1

  def save(self, match_path, show_max=DEFAULT_MATCHES_TO_DRAW):
    if self.good_matches is None:
      raise "Please run match before calling save"
    if (len(self.good_matches) > 0):
      # print("saving " + match_path+self.basepath())
      good=[]
      sgood = sorted(self.good_matches, key = lambda x:x.distance)
      nshow = len(sgood) if show_max == 0 else show_max
      img3 = cv2.drawMatches(self.img1.img,self.img1.kp,self.img2.img,self.img2.kp,sgood[:nshow], None, flags=2)
      cv2.imwrite(match_path + self.basepath(), img3)

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
parser.add_argument("-M", "--maybe", action='store_true', help="Only save inspection images for uncertain matches (maybe matches)")
parser.add_argument("-g", "--giova_thr", action='store', type=float, default=0.0, help="Loosen the Lowe Key point selection condition for points whose distance d<d_min + GIOVA_THR*(d_max - d_min)")
parser.add_argument("-w", "--nolowe", action='store_true', help="Use simpler matching method exclusively base on distance of NN keypoints and homography")
parser.add_argument("page", help="A file or a folder with 'page' images")
parser.add_argument("logo", help="A file or a folder with 'logo' images")
opts = parser.parse_args()

# validate match dir and evetually create the various folder that are needed
if opts.matchdir is not None:
  if opts.maybe:
    dirs=[opts.matchdir, opts.matchdir+"/maybe"]
  else:
    dirs=[opts.matchdir, opts.matchdir+"/maybe", opts.matchdir+"/all", opts.matchdir+"/yes", opts.matchdir+"/no"]
  for d in dirs:
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

# -----------------------------------
many_pages = (len(page_paths)>1)
many_logos = (len(logo_paths)>1)
verbose=(many_pages or many_logos)
save_all_matches = not (opts.maybe or opts.matchdir is None)
save_maybe_only  = opts.maybe and opts.matchdir is not None

if (opts.verbose):
  print(opts)
  print("many_pages: " + ("Y" if many_pages else "N" ))
  print("many_logos: " + ("Y" if many_logos else "N" ))
  print("save_all_matches: " + ("Y" if save_all_matches else "N" ))
  print("save_maybe_only: "  + ("Y" if save_maybe_only else "N" ))

# --------------------------------------------------------

# Precompute keypoint on all the logos
logos=[]
for logo_path in logo_paths:
  try:
    logo = MImage(logo_path)
    logos.append(logo)
  except:
    print("Invalid logo found in " + logo_path, file=sys.stderr)
    pass


for page_path in page_paths:

  try:
    page=MImage(page_path)
  except:
    print("Skipping invalid page found in " + page_path, file=sys.stderr)
    continue

  if (many_pages and opts.verbose): print("\n"+page_path)

  max_score=0
  best_m=None
  for logo in logos:
    m=Matcher(page, logo)
    if (opts.nolowe):
      score = m.match_simpler()
    else:
      score = m.match(giova_thr=opts.giova_thr)

    # print(page, logo, MIN_MATCH_COUNT, ypath)
    if (score > max_score): 
      max_score = score
      best_m = m

    if (many_logos and opts.verbose): print("%-20s %-20s %2d" % ("", logo.name, score))

    if (save_all_matches): 
      m.save(opts.matchdir + "/all/", opts.show_upto)

    m=None

  ans=""
  if max_score < opts.no_below:
    ans="no"
  else:
    if max_score > opts.yes_above:
      ans="yes"
    else:
      ans="maybe"
      if (save_maybe_only):
        best_m.save(opts.matchdir + "/maybe/", opts.show_upto)
  
  if (verbose):
    logoname = best_m.logo().name if best_m is not None else "NO_MATCHES"
    print("%-40s %-40s %3d      %s" % (page.name, logoname, max_score, ans))
  else:
    print(max_score)

  if save_all_matches:
    lpath=opts.matchdir + "/" + ans + "/" + best_m.basepath()
    os.symlink("../all/"+best_m.basepath(), lpath)

  page=None
  best_m=None