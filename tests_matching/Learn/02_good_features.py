# https://docs.opencv.org/3.4/d4/d8c/tutorial_py_shi_tomasi.html
import cv2
import numpy as np

# filename = 'logo/gray/c280.jpg'
# gray = cv2.imread(filename)

filename = 'in/logo.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)

cv2.imwrite('out/features.png',img)