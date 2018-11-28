# https://docs.opencv.org/3.4/df/dd2/tutorial_py_surf_intro.html
# Surf is a faster algorithm for SIFT
import cv2
import numpy as np

# filename = 'logo/gray/c280.jpg'
# gray = cv2.imread(filename)

filename = 'in/logo.jpg'
img = cv2.imread(filename)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

surf = cv2.xfeatures2d.SURF_create(400)
# print( surf.getHessianThreshold() )
# reduce number of points (for display purpose, in actual cases, it is better to have a value 300-500)
# surf.setHessianThreshold = 20000

# use larger (128 instead of 64) size for description (check with des.shape)
surf.setExtended(True)

# kp:  list of keypoints
# des: numpy array size(kp)x128 "describing" key points
kp, des = surf.detectAndCompute(img,None)

# out_img = cv2.imread(filename)
out_img=cv2.drawKeypoints(img, kp, None, (255,0,0), 4)
cv2.imwrite('out/surf_keypoints.jpg',out_img)

surf.setUpright(True)
kp, des = surf.detectAndCompute(img,None)
out_img=cv2.drawKeypoints(img, kp, None, (255,0,0), 4)
cv2.imwrite('out/surf_keypoints_upright.jpg',out_img)


