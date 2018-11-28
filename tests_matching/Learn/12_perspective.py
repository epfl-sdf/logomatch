import numpy as np
import cv2


h,w = 100,200
pts = np.float32([ [0,0],[0,h],[w,h],[w,0] ]).reshape(-1,1,2)
# pts = np.float32([ [0,0],[0,h],[w,h],[w,0] ]).reshape(-1,1,2)



# w =  M_31 * x + M_32 * y + M_33
# X = (M_11 * x + M_12 * y + M_13 ) / w
# Y = (M_21 * x + M_22 * y + M_23 ) / w
# M_11 M_12 M_13
# M_21 M_22 M_23
# M_31 M_32 M_33
M=np.array([
  [ 0.0, 1.0, 0.0],
  [ 1.0, 0.0, 0.0],
  [ 0.0, 0.0, 1.0],
])

dst = cv2.perspectiveTransform(pts,M)

print(pts[0], dst[0])
print(pts[1], dst[1])
print(pts[2], dst[2])
print(pts[3], dst[3])

d1 = np.linalg.norm(dst[1])
print(d1)
# d2 = dst[3] - dst[1]
