# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import cv2
import numpy as np

SHOW_MATCHES=10

FLANN_INDEX_KDTREE = 1

# FLANN base matcher needs two dictionaries as input (search_params and index_params)
search_params = dict(checks=50)

# For SIFT, SURF etc.
index_params1 = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)

flann = cv2.FlannBasedMatcher(index_params1, search_params)

img1 = cv2.imread('in/logo.png')
img2 = cv2.imread('in/page.png')

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

matches = flann.knnMatch(des1,des2, k=2)
matches = sorted(matches, key = lambda x:x[0].distance)

good=[]
for m, n in matches:
  if m.distance < 0.75 * n.distance:
    good.append([m])

# Draw first 10 matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/sift_flan_knn_matches.jpg', img3)

print("Number of good matches: %d" % len(good))


