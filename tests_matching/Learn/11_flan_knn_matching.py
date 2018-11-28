# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import cv2
import numpy as np

SHOW_MATCHES=10

FLANN_INDEX_KDTREE = 1
FLANN_INDEX_LSH = 6

# FLANN base matcher needs two dictionaries as input (search_params and index_params)
search_params = dict(checks=50)

# For SIFT, SURF etc.
index_params1 = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)

# For ORB
index_params2= dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)

flann_sift = cv2.FlannBasedMatcher(index_params1, search_params)
flann_orb  = cv2.FlannBasedMatcher(index_params2, search_params)

img1 = cv2.imread('in/logo.jpg', 0)
img2 = cv2.imread('in/page.jpg', 0)

# # ------------------------------------------ ORB
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

matches = flann_orb.knnMatch(des1,des2, k=2)
matches = sorted(matches, key = lambda x:x[0].distance)

good=[]
for m, n in matches:
  if m.distance < 0.75 * n.distance:
    good.append([m])

# Draw first 10 matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/orb_flan_knn_matches.jpg', img3)

# ------------------------------------------ SIFT

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

matches = flann_sift.knnMatch(des1,des2, k=2)
matches = sorted(matches, key = lambda x:x[0].distance)

good=[]
for m, n in matches:
  if m.distance < 0.75 * n.distance:
    good.append([m])

# Draw first 10 matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/sift_flan_knn_matches.jpg', img3)



