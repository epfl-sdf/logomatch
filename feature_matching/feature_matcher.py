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

import os.path
import glob
import sys
import numpy as np
import cv2
import argparse
import signal
from termcolor import colored

DOWNGRAY = False
MATCH_EXT="jpg"
DEFAULT_YES_ABOVE = 8
DEFAULT_NO_BELOW  = 6
DEFAULT_MATCHES_TO_DRAW = 50

class MImage():

  # class variables / constants
  sift = cv2.xfeatures2d.SIFT_create()

  def __init__(self, in_path, image=None):
    self.path = in_path
    self.name = os.path.splitext(os.path.basename(self.path))[0]

    if image is None:
      if DOWNGRAY:
        img_rgb = cv2.imread(self.path)
        self.img = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
      else:
        self.img = cv2.imread(self.path)
    else:
      self.img = image

    if DOWNGRAY:
      self.h, self.w = self.img.shape
    else:
      self.h, self.w, self.depth = self.img.shape

    self.kp, self.des = MImage.sift.detectAndCompute(self.img,None)
    # print("%20s  %d" % (self.name, len(self.kp)))

  def nk(self):
    return(len(self.kp))

  def width(self):
    return self.w

  def height(self):
    return self.h

  def arf(self):
    m=2.0/(self.h + self.w)
    return np.float32([m*self.w, m*self.h])

  def parts(self):
    hc = min(self.h/3, 250)
    parts = []
    parts.append(MImage(self.name+"_top.png", image=self.img[0:hc,0:self.w]))  # top
    parts.append(MImage(self.name+"_cen.png", image=self.img[hc:self.h-hc, 0:self.w]))    # center
    parts.append(MImage(self.name+"_bot.png", image=self.img[self.h-hc:self.h,0:self.w]))      # bottom
    return(parts)

class Matcher():

  # class variables / constants
  GIOVA_FACTOR = 0.9         # (Failed) attempt to do better than Lowe using the fact that we have 
  GIOVA_THRESHOLD = 0        # undeformed logo.

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
    self.zone = None
    self.good_matches = None
    self.invalid = False
    try:
      self.matches = Matcher.flann.knnMatch(self.img1.des,self.img2.des,k=2)
    except:
      self.matches=None
      self.good_matches=[]

  def match(self, 
            lowe_factor  = None,
            giova_thr    = 0,
            geofix       = 0,
            minkpdist    = 0,
            mingdisp     = 0,
            maxgdisp     = 0,
          ):

    if lowe_factor is None:
      lowe_factor = Matcher.LOWE_FACTOR

    # The giova_ stuff is a (failed) attempt to exploit the fact that we know that our logo
    # is not deformed (rotation, perspective). So, we use a less strict Lowe threshold 
    # (giova_factor > lowe_factor) but put an upper bound on the NN (giova_maxdist).
    # For giova_factor==1.0 we will kill Lowe and just count the number of matches that are
    # within a given distance. Preliminary tests show that this does not work at all.
    giova_factor = (1.0 + lowe_factor)/2,
    if self.matches is None: return 0

    if (giova_thr > 0):
      dmin = min(self.matches, key=lambda v: v[0].distance)[0].distance
      dmax = max(self.matches, key=lambda v: v[0].distance)[0].distance
      giova_maxdist = dmin + giova_thr * (dmax - dmin)
    else:
      giova_maxdist = 0.0



    dst_pts = []
    lowe_matches=[]
    for m,n in self.matches:
      if m.distance < lowe_factor*n.distance or (m.distance < giova_maxdist and m.distance < giova_factor*n.distance):
        if minkpdist > 0:
          # Filter based on distance of match points in the second image. This is to
          # prevent having many similar key points in the frist image match the same zone in the second image.
          # A new match is added only if the point in the second image is far enough from all previously added points.
          ok=True
          p = np.float32(self.img2.kp[m.trainIdx].pt)
          for p0 in dst_pts:
            d = np.linalg.norm(p - p0)
            ok = ok and (d > 5)
          if ok:
            dst_pts.append(p)
            lowe_matches.append(m)
        else:
          lowe_matches.append(m)

    self.homographyFilter(lowe_matches, geofix, mingdisp, maxgdisp)

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

  def homographyFilter(self, mm, geofix=0, mingdisp=0, maxgdisp=0):

    matches=[]
    if maxgdisp == 0 or ( (maxgdisp == 1) and (len(mm) < Matcher.MIN_STDDEV_COUNT) ) or ( (maxgdisp > 1) and len(mm) < Matcher.MIN_GDIST_COUNT ):
      matches = mm
    else:
      # Filter based on dispersion of match points. Two possible cryteria
      # 1. when (maxgdisp == 1): use standard deviation as cut-off
      # 2. when (maxgdisp  > 1): use given value (adapted to first image aspect ratio)
      pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in mm ]).reshape(-1,2)
      cen = np.mean(pts, (0))
      if (maxgdisp == 1):
        maxdev = Matcher.STDDEV_FACTOR * np.std(pts, (0))
      else:
        maxdev = maxgdisp * self.img2.arf()

      i=0
      for p in pts:
        e = maxdev - np.abs(p - cen)
        if (e[0] > 0 and e[1] > 0):
          matches.append(mm[i])
        i=i+1

      if mingdisp > 0 and len(matches) > 0:
        pts = np.float32([ self.img2.kp[m.trainIdx].pt for m in matches ]).reshape(-1,2)
        dev = np.std(pts, (0))
        mindev = mingdisp * self.img2.arf()
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
      if (len(self.good_matches) < geofix and self.zone is not None):
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
parser.add_argument("-p", "--partials", action='store', type=int, default=0, help="Try to do the matching with parts of the page (default=0)")
parser.add_argument("-g", "--geofix", action='store', type=int, default=0, help="Try to exclude matches with unlikely geometry when score < geofix (default=0)")
parser.add_argument("-D", "--maxgdisp", action='store', default=0, type=int, help="Remove all the keypoints that are more than maxgdisp from center of mass. If D<3 then it is multiplied by stddev")
parser.add_argument("-E", "--mingdisp", action='store', default=0, type=int, help="If dispersion of keypoints is smaller than this, match is not valid")
parser.add_argument("-K", "--minkpdist", action='store', default=0, type=int, help="Reject matches that are closer than minkpdist from other points in the page")

parser.add_argument("-s", "--show_upto", action='store', type=int, default=DEFAULT_MATCHES_TO_DRAW, help="Number of matches to show in the inspection image (default %d)" % DEFAULT_MATCHES_TO_DRAW)
parser.add_argument("-l", "--lowe_factor", action='store', type=float, default=Matcher.LOWE_FACTOR, help="Set the Lowe factor: keypoint is kept only if distance(NN) < LF * distance(NNN) (default %f" % Matcher.LOWE_FACTOR)
parser.add_argument("-t", "--giova_thr", action='store', type=float, default=0.0, help="Loosen the Lowe Key point selection condition for points whose distance d<d_min + GIOVA_THR*(d_max - d_min)")
parser.add_argument("-w", "--nolowe", action='store_true', help="Use simpler matching method exclusively base on distance of NN keypoints and homography")
parser.add_argument("page", help="A file or a folder with 'page' images")
parser.add_argument("logo", help="A file or a folder with 'logo' images")
opts = parser.parse_args()

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
many_pages = (len(page_paths)>1)
many_logos = (len(logo_paths)>1)
verbose=(many_pages or many_logos)

save_all   = opts.verbose and opts.matchdir is not None
save_maybe = not (opts.quiet or save_all or opts.matchdir is None)
save_yesno = not (opts.quiet or save_all or opts.maybe or opts.matchdir is None)

# print("save_all:   " + ("Y" if save_all else "N" ) )
# print("save_maybe: " + ("Y" if save_maybe else "N" ) )
# print("save_yesno: " + ("Y" if save_yesno else "N" ) )
# print("verbose:           " + ("Y" if opts.verbose else "N" ))
# print("quiet:             " + ("Y" if opts.quiet else "N" ))
# if (opts.verbose):
#   print(opts)
#   print("many_pages: " + ("Y" if many_pages else "N" ))
#   print("many_logos: " + ("Y" if many_logos else "N" ))

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
  page_count=page_count+1
  sys.stderr.write("%d/%d\n" % (page_count, page_total))
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

    try:
      if (opts.nolowe):
        score = m.match_simpler()
      else:
        score = m.match(minkpdist=opts.minkpdist, geofix=opts.geofix, mingdisp=opts.mingdisp, maxgdisp=opts.maxgdisp, lowe_factor=opts.lowe_factor, giova_thr=opts.giova_thr)
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

    if (many_logos and opts.verbose): print("%-20s %-20s %2d   %3d" % ("", logo.name, score, xscore))

    if save_all:
      m.save(opts.matchdir + "/all/", opts.show_upto)

    # In case no match have a positive score we just take one at random (the last)
    if best_m is None: best_m = m

    m=None

  if (max_score < opts.partials):

    max_score2 = max_score
    best_m2 = None
    for part in page.parts():
      for logo in logos:
        m = Matcher(part, logo)
        score = m.match(minkpdist=opts.minkpdist, geofix=opts.geofix, mingdisp=opts.mingdisp, maxgdisp=opts.maxgdisp, lowe_factor=opts.lowe_factor, giova_thr=opts.giova_thr)
        if (score >= max_score2): 
          max_score2 = score
          best_m2 = m
        if (many_logos and opts.verbose): print("%20s %-20s %2d" % ("part", logo.name, score))
        if save_all:
          m.save(opts.matchdir + "/all/", opts.show_upto)
        m = None
    if max_score2 > max_score:
      max_score = max_score2
      best_m = best_m2

  ans=""
  if max_score < opts.no_below:
    ans=colored("no", "red") if opts.color else "no"
    if save_yesno:
      best_m.save(opts.matchdir + "/no/", opts.show_upto)
  else:
    if max_score > opts.yes_above:
      ans=colored("yes", "green") if opts.color else "yes"
      if save_yesno:
        best_m.save(opts.matchdir + "/yes/", opts.show_upto)
    else:
      ans=colored("maybe", "blue") if opts.color else "maybe"
      if save_maybe:
        best_m.save(opts.matchdir + "/maybe/", opts.show_upto)
  
  if (verbose):
    logoname = best_m.logo().name if best_m is not None else "NO_MATCHES"
    print("%-40s %-40s %3d      %s" % (page.name, logoname, max_score, ans))
  else:
    print(max_score)

  if save_all and best_m is not None:
    lpath=opts.matchdir + "/" + ans + "/" + best_m.basepath()
    os.symlink("../all/"+best_m.basepath(), lpath)

  page=None
  best_m=None

exit(0)
