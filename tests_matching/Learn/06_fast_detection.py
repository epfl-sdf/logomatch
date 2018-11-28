# https://docs.opencv.org/3.4/df/d0c/tutorial_py_fast.html
# an even faster algorithm for real time
import cv2
import numpy as np

# filename = 'logo/gray/c280.jpg'
# gray = cv2.imread(filename)

filename = 'in/logo.jpg'
img = cv2.imread(filename)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector_create()

# find and draw the keypoints
kp = fast.detect(img, None)

img2 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

# Print all default params
print( "Threshold: {}".format(fast.getThreshold()) )
print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
print( "neighborhood: {}".format(fast.getType()) )
print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )
cv2.imwrite('out/fast_keypoints_with_nomax.png',img2)

# Disable nonmaxSuppression
fast.setNonmaxSuppression(0)
kp = fast.detect(img,None)
print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
img3 = cv2.drawKeypoints(img, kp, None, color=(255,0,0))

cv2.imwrite('out/fast_keypoints_without_nomax.png',img3)



