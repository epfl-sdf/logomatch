# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import cv2
import numpy as np

SHOW_MATCHES=10

img1 = cv2.imread('in/logo.jpg', 0)
img2 = cv2.imread('in/page.jpg', 0)

# create BFMatcher object
# BFMatcher first param is the norm to be used to compare descriptors
# Use cv2.NORM_L2 for SIFT, SURF, FAST) and cv2_NORM_HAMMING for ORB
bf_ham = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
bf_l2 = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

# ------------------------------------------ ORB
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)


# Match descriptors. DMatch object has following attributes:
# DMatch.distance: Distance between descriptors. The lower, the better it is.
# DMatch.trainIdx: Index of the descriptor in train descriptors
# DMatch.queryIdx: Index of the descriptor in query descriptors
# DMatch.imgIdx:   Index of the train image.

matches = bf_ham.match(des1,des2)

# Sort them in the order of their distance.

matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/orb_bf_matches.jpg', img3)

# ------------------------------------------ SURF

surf = cv2.xfeatures2d.SURF_create(400)
# use larger (128 instead of 64) size for description (check with des.shape)
surf.setExtended(True)

kp1, des1 = surf.detectAndCompute(img1,None)
kp2, des2 = surf.detectAndCompute(img2,None)

# create BFMatcher object
# BFMatcher first param is the norm to be used to compare descriptors
# Use cv2.NORM_L2 for SIFT, SURF, FAST) and cv2_NORM_HAMMING for ORB

# Match descriptors.
matches = bf_l2.match(des1,des2)

# Sort them in the order of their distance.

matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/surf_bf_matches.jpg', img3)

# ------------------------------------------ SIFT

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# create BFMatcher object
# BFMatcher first param is the norm to be used to compare descriptors
# Use cv2.NORM_L2 for SIFT, SURF, FAST) and cv2_NORM_HAMMING for ORB

# Match descriptors.
matches = bf_l2.match(des1,des2)

# Sort them in the order of their distance.

matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/sift_bf_matches.jpg', img3)





