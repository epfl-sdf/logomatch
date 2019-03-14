# docker run -v /Users/cangiani/iDevProjects/logomatch/feature_matching:/wd opencv learn.py
import cv2
import numpy as np
from timeit import default_timer as timer

USEORB=True

# -------------------------------------------------- Common Functions
def homographyFilter(kp1, kp2, matches):
  if len(matches) < 4:
    return []

  p2 = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
  p1 = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)

  M, mask = cv2.findHomography(p1, p2, cv2.RANSAC,5.0)
  select_mask = mask.ravel().tolist()

  good = []
  for i, m in enumerate(select_mask):
    if (m==1):
      good.append(matches[i])
  return good

def loweFilter(matches):
  good = []
  for m,n in matches:
    if m.distance < 0.75*n.distance:
      good.append(m)
  return good

# -------------------------------------------------------- Main

orb = cv2.ORB_create(nfeatures=1000)
surf = cv2.xfeatures2d.SURF_create(1000)
sift = cv2.xfeatures2d.SIFT_create()

img1 = cv2.imread('logos_im/c_360.png',0)          # queryImage
img2 = cv2.imread('pages/debug/http_blockchain-school2019.png',0) # trainImage

# BFMatcher for ORB features and for SIFT/SURF
bf1 = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
bf2 = cv2.BFMatcher()

res = []

# ------------------------------------------------------ orb + BF

t0=timer()
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
t1=timer()
matches = bf1.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)
t2=timer()

good = homographyFilter(kp1, kp2, matches)
t3=timer()

# Just take the first 10 matches
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:50],None,flags=2)
cv2.imwrite("learn/orb_bf.png", img3)

res.append({
  "title": "ORB + BF",
  "nkp1": len(kp1), 
  "nkp2": len(kp2),
  "nmatch": len(matches),
  "nlowe": 0,
  "ngood": 0,
  "tdetect": t1-t0,
  "tmatch": t2-t1,
  "tlowe": 0,
  "thomo": t3-t2,
})

# ------------------------------------------------------ sift + BF + lowe
t0=timer()
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
t1=timer()
matches = bf2.knnMatch(des1,des2, k=2)
t2=timer()

lowe = loweFilter(matches)
t3=timer()

good = homographyFilter(kp1, kp2, lowe)
t4=timer()

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,flags=2)
cv2.imwrite("learn/sift_bf_lowe.png", img3)

res.append({
  "title": "SIFT + BF + LOWE",
  "nkp1": len(kp1), 
  "nkp2": len(kp2),
  "nmatch": len(matches),
  "nlowe": len(lowe),
  "ngood": len(good),
  "tdetect": t1-t0,
  "tmatch": t2-t1,
  "tlowe": t3-t2,
  "thomo": t4-t2,
})

# ------------------------------------------------------ surf + BF + lowe
t0=timer()
kp1, des1 = surf.detectAndCompute(img1,None)
kp2, des2 = surf.detectAndCompute(img2,None)
t1=timer()
matches = bf2.knnMatch(des1,des2, k=2)
t2=timer()

lowe = loweFilter(matches)
t3=timer()

good = homographyFilter(kp1, kp2, lowe)
t4=timer()

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,flags=2)
cv2.imwrite("learn/surf_bf_lowe.png", img3)

res.append({
  "title": "SURF + BF + LOWE",
  "nkp1": len(kp1), 
  "nkp2": len(kp2),
  "nmatch": len(matches),
  "nlowe": len(lowe),
  "ngood": len(good),
  "tdetect": t1-t0,
  "tmatch": t2-t1,
  "tlowe": t3-t2,
  "thomo": t4-t2,
})

# ----------------------------------------------------
kss=["title"] 
ksd=["nkp1", "nkp2", "nmatch", "nlowe", "ngood"] 
kst=["tdetect", "tmatch", "tlowe", "thomo"] 
ks = kss + ksd + kst

for k in ks:
  print("%16s" % k, end='')
print()

for r in res:
  for k in kss:
    print("%16s" % r[k], end='')
  for k in ksd:
    print("%16d" % r[k], end='')
  for k in kst:
    print("%16.4f" % r[k], end='')
  print()
