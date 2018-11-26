# https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html
# sift and surf are patented. Orb is a free alternative
import cv2
import numpy as np

# filename = 'logo/gray/c280.jpg'
# gray = cv2.imread(filename)

filename = 'in/logo.jpg'
img = cv2.imread(filename, 0)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create()

# kp:  list of keypoints
# des: numpy array size(kp)x128 "describing" key points
# kp, des = orb.detectAndCompute(img,None)
kp = orb.detect(img, None)
kp, des = orb.compute(img, kp)

out_img=cv2.drawKeypoints(img, kp, None, (255,0,0), 0)
cv2.imwrite('out/orb_keypoints.jpg',out_img)


