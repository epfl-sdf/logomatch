# https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
import cv2
import numpy as np

SHOW_MATCHES=10

img1 = cv2.imread('in/logo.jpg', 0)
img2 = cv2.imread('in/page.jpg', 0)


sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

bf_l2 = cv2.BFMatcher(cv2.NORM_L2)
matches = bf_l2.knnMatch(des1,des2, k=2)

# matches = sorted(matches, key = lambda x:x[0].distance)

good=[]
for m, n in matches:
  if m.distance < 0.75 * n.distance:
    good.append([m])

# Draw first 10 matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/sift_bf_knn_matches.jpg', img3)



matches = sorted(matches, key = lambda x:x[0].distance)

good=[]
for m, n in matches:
  if m.distance < 0.75 * n.distance:
    good.append([m])

# Draw first 10 matches.
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:SHOW_MATCHES], None, flags=2)

cv2.imwrite('out/sift_bf_knn_matches_sorted.jpg', img3)
