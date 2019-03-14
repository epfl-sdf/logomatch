# Run with
# rm match/no/*
# rm match/yes/*
# docker run -it -v $PWD:/app -w=/app valian/docker-python-opencv-ffmpeg python test3.py
# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_sift_intro/py_sift_intro.html

# park links for more study
# https://docs.opencv.org/master/d5/dae/tutorial_aruco_detection.html
# http://answers.opencv.org/question/25772/logo-detection-techniques/
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
# https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
# https://www.pyimagesearch.com/practical-python-opencv/?src=resource-guide-conf

import argparse
import cv2
# import gc
import glob
import numpy as np
import os.path
import resource
import sys
import signal
from termcolor import colored
from timeit import default_timer as timer

DOWNGRAY = False
MATCH_EXT="jpg"
DEFAULT_YES_ABOVE = 8
DEFAULT_NO_BELOW  = 6
DEFAULT_MATCHES_TO_DRAW = 50

class MImage():

  # class variables / constants
  # sift = cv2.ORB_create()
  # sift = cv2.xfeatures2d.SURF_create(2000)
  # sift = cv2.xfeatures2d.SIFT_create(nfeatures=500)
  sift = cv2.xfeatures2d.SIFT_create()

  def __init__(self, in_path, image=None):
    self.path = in_path
    self.name = os.path.splitext(os.path.basename(self.path))[0]
    self.need_dac = True
    if image is None:
      try:
        if DOWNGRAY:
          img_rgb = cv2.imread(self.path)
          self.img = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
        else:
          self.img = cv2.imread(self.path)
      except Exception as err:
        print("!! Error loading image " + page_path, file=sys.stderr)
        raise err
    else:
      self.img = image

    if DOWNGRAY:
      self.h, self.w = self.img.shape
    else:
      self.h, self.w, self.depth = self.img.shape

  def dac(self):
    if (self.need_dac):
      self.kp, self.des = MImage.sift.detectAndCompute(self.img,None)
      self.need_dac = False

  def nk(self):
    return(len(self.kp))

  def width(self):
    return self.w

  def height(self):
    return self.h

  def arf(self):
    m=2.0/(self.h + self.w)
    return np.float32([m*self.w, m*self.h])

  # def parts(self):
  #   hc = min(self.h/3, 250)
  #   parts = []
  #   parts.append(MImage(self.name+"_top.png", image=self.img[0:hc,0:self.w]))  # top
  #   parts.append(MImage(self.name+"_cen.png", image=self.img[hc:self.h-hc, 0:self.w]))    # center
  #   parts.append(MImage(self.name+"_bot.png", image=self.img[self.h-hc:self.h,0:self.w]))      # bottom
  #   return(parts)

  # Split the image into smaller parts (PH=height, PS=step => there will be PH-PS overlap)
  def parts(self, ph=600, ps=400):
    np=int(0.5 + (self.h - ph)/ps)
    parts=[]
    for i in range(0, np):
      y0 = i * ps
      y1 = min(y0+ph, self.h)
      nn = "%s_p%02d" % (self.name, i)
      parts.append(MImage(nn, image=self.img[y0:y1,0:self.w]))
    return(parts)

class Matcher():

  LOWE_FACTOR = 0.7          # For each point in logo 2 possible matches are detected in the page
                             # image. Points are kept only when the distance of the first match is 
                             # considerably (LOWE_FACTOR) smaller than the one or the second match
  MIN_MATCH_COUNT = 4        # min no. points for homography to work
  STDDEV_FACTOR = 1.0        # drop points outside STDDEV_FACTOR * Sigma from mean
  MIN_STDDEV_COUNT = 10      # min number of points for a reasonable mean/stdev
  MIN_GDIST_COUNT = 4       # min number of points for a reasonable mean


  FLANN_INDEX_KDTREE = 1     # 1 for SIFT, SURF; 6 for ORB   DO NOT TOUCH!
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)
  flann = cv2.FlannBasedMatcher(index_params, search_params)

  def __init__(self, img2, img1):
    self.img1 = img1
    self.img2 = img2
    self.img1.dac()
    self.img2.dac()
    self.zone = None
    self.good_matches = None
    self.invalid = False
    try:
      self.matches = Matcher.flann.knnMatch(self.img1.des,self.img2.des,k=2)
    except:
      self.matches=None
      self.good_matches=[]

  def match(self, opts):

    if self.matches is None: return 0

    dst_pts = []
    lowe_matches=[]
    for m,n in self.matches:
      if m.distance < opts.lowe_factor*n.distance:
        if opts.minkpdist > 0:
          # Filter based on distance of match points in the second image. This is to
          # prevent having many similar key points in the frist image match the same zone in the second image.
          # A new match is added only if the point in the second image is far enough from all previously added points.
          # Quite useless. Similarly I have tried to get rid of matches that are on a completely different region of
          # the page by giving a chance to the second best match when the first one is geometrically far from the center
          # of gravity of the matched logo (computed from a first standard run)
          # TODO: remove this crap
          ok=True
          p = np.float32(self.img2.kp[m.trainIdx].pt)
          for p0 in dst_pts:
            d = np.linalg.norm(p - p0)
            ok = ok and (d > opts.minkpdist)
          if ok:
            dst_pts.append(p)
            lowe_matches.append(m)
        else:
          lowe_matches.append(m)

    self.homographyFilter(lowe_matches, opts)
    return self.score()

  def homographyFilter(self, mm, opts):
    matches=[]
    if opts.maxgdisp == 0 or ( (opts.maxgdisp == 1) and (len(mm) < Matcher.MIN_STDDEV_COUNT) ) or ( (opts.maxgdisp > 1) and len(mm) < Matcher.MIN_GDIST_COUNT ):
      matches = mm
    else:
      # Filter based on dispersion of match points. Two possible cryteria
      # 1. when (maxgdisp == 1): use standard deviation as cut-off
      # 2. when (maxgdisp  > 1): use given value (adapted to first image aspect ratio)
      pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in mm ]).reshape(-1,2)
      cen = np.mean(pts, (0))
      if (opts.maxgdisp == 1):
        maxdev = Matcher.STDDEV_FACTOR * np.std(pts, (0))
      else:
        maxdev = opts.maxgdisp * self.img2.arf()

      i=0
      for p in pts:
        e = maxdev - np.abs(p - cen)
        if (e[0] > 0 and e[1] > 0):
          matches.append(mm[i])
        i=i+1

      if opts.mingdisp > 0 and len(matches) > 0:
        pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in matches ]).reshape(-1,2)
        dev = np.std(pts, (0))
        mindev = opts.mingdisp * self.img2.arf()
        if (dev[0] < mindev[0] or dev[1] < mindev[1]):
          matches = []

    if len(matches) == 0:
      self.good_matches = []
      self.invalid = True
      return

    # If enough points, a second selection is done by the Homography algorithm that keeps
    # only the points that can be linked geometrically
    if len(matches) > Matcher.MIN_MATCH_COUNT:

    #   if (maxgdisp>0):
    #     g=np.sum(dst_pts, (0,1))/len(matches)
        
      dst_pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
      src_pts = np.float32([ self.img1.kp[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)

      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      select_mask = mask.ravel().tolist()
      self.good_matches = []
      for i, m in enumerate(select_mask):
        if (m==1):
          self.good_matches.append(matches[i])
      try:
        h,w = self.logo().img.shape[:2]
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        self.zone = np.int32(cv2.perspectiveTransform(pts,M))
      except:
        print("!!no zone")
        self.zone = None

      # Filter based on the geometry of the resulting matched image. This also
      # is not very usefull in the case of the logo because it contains text and
      # is very easy to swap two similar character graces. Therefore the rectangle
      # defining the match results often badly deformed although the match is not bad.
      if (len(self.good_matches) < opts.geofix and self.zone is not None):
        # Negative values in the rotation matrix indicates some bad transofmration that will heavily deform the rectangle ?
        # if (M[0,0] < 0 or M[1,1] < 0 or M[0,1] < 0 or M[1,0] < 0):
        #   self.good_matches = []
        # If the diagonals are too different it is no longer a rectangle!
        # Also we expect a logo to be larger than 25px in diagonal
        d1 = np.linalg.norm(self.zone[2] - self.zone[0])
        d2 = np.linalg.norm(self.zone[3] - self.zone[1])
        if (d1 < 25 or d2 < 25):
          self.invalid = True
        else:
          # accept upto 10% difference in the diagonals
          dd = 2 * abs(d1-d2)/(d1+d2)
          self.invalid = (dd>0.1)
          # check correct order in corners
          # self.zone[0][0][0] < self.zone[2][0][0]
          # self.zone[0][0][0] < self.zone[3][0][0]
          # self.zone[1][0][0] < self.zone[2][0][0]
          # self.zone[1][0][0] < self.zone[3][0][0]
    else:
      self.good_matches = matches

  def score(self):
    if self.good_matches is None:
      return None
    else:
      if (self.invalid):
        return 0
      else:
        # Give a bit more points to logos with fewer number of keypoints
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
      if self.zone is None:
        img3 = self.img2.img
      else:
        img3 = cv2.polylines(self.img2.img.copy(),[self.zone],True,255,3, cv2.LINE_AA)
      # flags: 0=draw all the points without size, 1=crash, 2=only good matches without size, 4=draw all points with circle proportional to NN distance
      img4 = cv2.drawMatches(self.img1.img,self.img1.kp,img3,self.img2.kp,sgood[:nshow], None, flags=2)


      cv2.imwrite(match_path + self.basepath(), img4)

# ----------------------------------------------------
def crepa():
  exit(1)

def best_match(page, logos, opts):
  t0 = timer()
  max_score=0
  best_m=None
  for logo in logos:
    m=Matcher(page, logo)
    try:
      score = m.match(opts)
    except:
      if opts.verbose:
        print("!! Error matching");
      next

    if (opts.kpcorrect):
      xscore = (300 - logo.nk())/80
      score = max(0, score + xscore)
    else:
      xscore = 0

    # print(page, logo, MIN_MATCH_COUNT, ypath)
    if (score > max_score): 
      max_score = score
      best_m = m

    # if (many_logos and opts.verbose): sys.stderr.write("%-20s %-20s %2d   %3d    %8.5f\n" % ("", logo.name, score, xscore, match_time))
    # print("%-20s %-20s %2d   %3d\n" % ("", logo.name, score, xscore))

    # if save_all:
    #   m.save(opts.matchdir + "/all/", opts.show_upto)

    # In case no match have a positive score we just take one at random (the last)
    if best_m is None: best_m = m

    t1 = timer()
    if (opts.verbose): print("%-40s %-40s %3d     %8.4f" % (page.name, logo.name, max_score, t1-t0), file=sys.stderr)

    del m
  return max_score, best_m

signal.signal(signal.SIGTERM, crepa)

parser = argparse.ArgumentParser(
  prog = "logospotter",
  description = "Logo spotter",
  epilog = """ This program scans one or more images ('page'), for presence of another image ('logo').
               If a folder of 'pages' is provided, it will scann all of them;
               If a folder of 'logos' is provided, it will search for the best match.
               There are various parameters to change the algorithm but the defaults are most probably the best choice.
           """
)
parser.add_argument("-v", "--verbose", action='store_true', help="Increase output level")
parser.add_argument("-q", "--quiet", action='store_true', help="Decrease output level. In particular, do not save match images.")
parser.add_argument("-n", "--no_below", action='store', type=int, default=DEFAULT_NO_BELOW, help="Below this threshold, images do not match (default %d)" % DEFAULT_NO_BELOW)
parser.add_argument("-y", "--yes_above", action='store', type=int, default=DEFAULT_YES_ABOVE, help="Below this threshold, images do not match (default %d)" % DEFAULT_YES_ABOVE)
parser.add_argument("-k", "--kpcorrect", action='store_true', help="Correct the score based on the number of key points of the logo (cropped logos have much fewer kps)")
parser.add_argument("-m", "--matchdir", action='store', help="Output directory for match images (mostly used for inspecting output while debugging)")
parser.add_argument("-M", "--maybe", action='store_true', help="Only save inspection images for uncertain matches (maybe matches)")
parser.add_argument("-c", "--color", action='store_true', help="Colorize output")
parser.add_argument("-p", "--parts", action='store', type=int, default=0, help="Split the image in sub images if the height is larger than given (default=0 means never split)")
parser.add_argument("-ph", "--partheight", action='store', type=int, default=1200, help="Height of the partial page (default=1200)")
parser.add_argument("-ps", "--partstep", action='store', type=int, default=1000, help="Height of the partial page (default=1000)")

parser.add_argument("-g", "--geofix", action='store', type=int, default=0, help="Try to exclude matches with unlikely geometry when score < geofix (default=0)")
parser.add_argument("-D", "--maxgdisp", action='store', default=0, type=int, help="Remove all the keypoints that are more than maxgdisp from center of mass. If D<3 then it is multiplied by stddev")
parser.add_argument("-E", "--mingdisp", action='store', default=0, type=int, help="If dispersion of keypoints is smaller than this, match is not valid")
parser.add_argument("-K", "--minkpdist", action='store', default=0, type=int, help="Reject matches that are closer than minkpdist from other points in the page (useless)")
parser.add_argument("-R", "--reslimit", action='store', default=1536, type=int, help="Limit memory usage to given number of Mb")

parser.add_argument("-s", "--show_upto", action='store', type=int, default=DEFAULT_MATCHES_TO_DRAW, help="Number of matches to show in the inspection image (default %d)" % DEFAULT_MATCHES_TO_DRAW)
parser.add_argument("-l", "--lowe_factor", action='store', type=float, default=Matcher.LOWE_FACTOR, help="Set the Lowe factor: keypoint is kept only if distance(NN) < LF * distance(NNN) (default %f" % Matcher.LOWE_FACTOR)
parser.add_argument("-t", "--giova_thr", action='store', type=float, default=0.0, help="Loosen the Lowe Key point selection condition for points whose distance d<d_min + GIOVA_THR*(d_max - d_min)")
parser.add_argument("page", help="A file or a folder with 'page' images")
parser.add_argument("logo", help="A file or a folder with 'logo' images")
opts = parser.parse_args()

lh = opts.reslimit * 1024 * 1024
ls = (opts.reslimit - 256) * 1024 * 1024
resource.setrlimit(resource.RLIMIT_DATA, (ls, lh))

# validate match dir and evetually create the various folder that are needed
if opts.matchdir is not None:
  if opts.maybe:
    dirs=[opts.matchdir, opts.matchdir+"/maybe"]
  else:
    dirs=[opts.matchdir, opts.matchdir+"/maybe", opts.matchdir+"/yes", opts.matchdir+"/no"]
  if opts.verbose:
    dirs.append(opts.matchdir+"/all")
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
# many_pages = (len(page_paths)>1)
# many_logos = (len(logo_paths)>1)
# verbose=(many_pages or many_logos)

# save_all   = opts.verbose and opts.matchdir is not None
# save_maybe = not (opts.quiet or save_all or opts.matchdir is None)
# save_yesno = not (opts.quiet or save_all or opts.maybe or opts.matchdir is None)

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

page_count=0
page_total=len(page_paths)
for page_path in page_paths:
  page_start = timer()
  page_count=page_count+1
  sys.stderr.write("%d/%d\n" % (page_count, page_total))
  try:
    page=MImage(page_path)
  except Exception as err:
    print(str(err))
    print("!! Skipping invalid page found in " + page_path)
    continue

  if (opts.parts > 0 and page.height() > opts.parts):
    max_score = 0
    for part in page.parts(opts.partheight, opts.partstep):
      score, match = best_match(part, logos, opts)
      if (score >= max_score):
        max_score = score
        best_m = match
      part = None
  else:
    max_score, best_m = best_match(page, logos, opts)


  ans=""
  if max_score < opts.no_below:
    ans=colored("no", "red") if opts.color else "no"
    best_m.save(opts.matchdir + "/no/", opts.show_upto)
  else:
    if max_score > opts.yes_above:
      ans=colored("yes", "green") if opts.color else "yes"
      best_m.save(opts.matchdir + "/yes/", opts.show_upto)
    else:
      ans=colored("maybe", "blue") if opts.color else "maybe"
      best_m.save(opts.matchdir + "/maybe/", opts.show_upto)
  
  logoname = best_m.logo().name if best_m is not None else "NO_MATCHES"
  # print("%-40s %-40s %3d      %s   %8.5f\n" % (page.name, logoname, max_score, ans, page_stop-page_start))
  print("%-40s %-40s %3d      %s" % (page.name, logoname, max_score, ans))
 
  page=None
  best_m=None

exit(0)
