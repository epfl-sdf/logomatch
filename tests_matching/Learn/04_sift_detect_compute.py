# https://docs.opencv.org/3.4/da/df5/tutorial_py_sift_intro.html
# This is like 03_sift_detection.pu but also computes the descriptors of the key point that is used for comparing images
import cv2
import numpy as np

# filename = 'logo/gray/c280.jpg'
# gray = cv2.imread(filename)

filename = 'in/logo.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()

# kp:  list of keypoints
# des: numpy array size(kp)x128 "describing" key points
kp, des = sift.detectAndCompute(gray,None)


out_img = cv2.imread(filename)
img=cv2.drawKeypoints(gray, kp, out_img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imwrite('out/sift_keypoints.jpg',out_img)