# https://docs.opencv.org/3.4/dc/d7d/tutorial_py_brief.html
# brief is used to generate smaller descriptor lists
import cv2
import numpy as np

# filename = 'logo/gray/c280.jpg'
# gray = cv2.imread(filename)

filename = 'in/logo.jpg'
img = cv2.imread(filename)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Initiate FAST detector
# fast = cv2.FastFeatureDetector_create()
star = cv2.xfeatures2d.StarDetector_create()

# find and draw the keypoints
# kp = fast.detect(img, None)
kp = star.detect(img, None)

img2 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

cv2.imwrite('out/star_features.png',img2)

brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
# compute the descriptors with BRIEF
kp, des = brief.compute(img, kp)

print( brief.descriptorSize() )
print( des.shape )