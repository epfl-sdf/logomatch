# USAGE
# python match.py --template cod_logo.png --images images

# import the necessary packages
import numpy as np
import argparse
import imutils
import glob
import os.path
import cv2
from skimage.measure import compare_ssim

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=True, help="Path to template image")
ap.add_argument("-i", "--images", required=True,
	help="Path to images where template will be matched")
ap.add_argument("-o", "--odir", required=True,
	help="Path to folder for matched images")
ap.add_argument("-v", "--visualize",
	help="Flag indicating whether or not to visualize each iteration")
ap.add_argument("-m", "--method", required=False, 
	help="Index of matching method 0-5", default=0)
ap.add_argument("-e", "--edged", action='store_true', required=False,
	help="Preprocess image with edge detection")
args = vars(ap.parse_args())

method = eval(methods[int(args["method"])])
method = cv2.TM_CCOEFF

odir=args["odir"]
if (not os.path.exists(odir)):
  os.mkdir(odir)

# load the image image, convert it to grayscale, and detect edges
template = cv2.imread(args["template"])
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
canny_template = cv2.Canny(template, 50, 200)
(tH, tW) = canny_template.shape[:2]
# cv2.imshow("Template", template)

# loop over the images to find the template in
for imagePath in glob.glob(args["images"] + "/*.jpg"):
	# load the image, convert it to grayscale, and initialize the
	# bookkeeping variable to keep track of the matched region
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	found = None

	# loop over the scales of the image
	for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break

		# detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
		if args["edged"]:
			edged = cv2.Canny(resized, 50, 200)
			result = cv2.matchTemplate(edged, canny_template, method)
		else:
			result = cv2.matchTemplate(resized, canny_template, method)

		minVal, maxVal, minLoc, maxLoc  = cv2.minMaxLoc(result)

		s=""
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			val = minVal
			if found is None or minVal < found[0]:
				found = (minVal, minLoc, r)
		else:
			val = maxVal
			if found is None or maxVal > found[0]:
				found = (maxVal, maxLoc, r)

		top_left = found[1]
		bottom_right = (top_left[0] + tW, top_left[1] + tH)


		# check to see if the iteration should be visualized
		if args.get("visualize", False):
			print("    %-32s  %5.2f  %8.4e  %8.4e" % (imagePath, scale, val, found[0]))
			# draw a bounding box around the detected region
			clone = np.dstack([edged, edged, edged])
			cv2.rectangle(clone, (top_left[0], top_left[1]),
				(bottom_right[0], bottom_right[1]), (0, 0, 255), 2)
			cv2.imshow("Visualize", clone)
			cv2.waitKey(0)


		# if we have found a new maximum correlation value, then ipdate
		# the bookkeeping variable


	# unpack the bookkeeping varaible and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
	(v, top_left, r) = found
	(startX, startY) = (int(top_left[0] * r), int(top_left[1] * r))
	(endX, endY) = (int((top_left[0] + tW) * r), int((top_left[1] + tH) * r))

	# draw a bounding box around the detected result and display the image
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	mpath = odir + "/" + os.path.basename(imagePath)
	cv2.imwrite(mpath, image)


	# cropped = resized[startX:endX, startY:endY]
	# print(cropped.shape[:2], template.shape[:2])

	# (score, diff) = compare_ssim(cropped, template, full=True)
	# print(score, diff)



	print("**  %-32s  %6.4f %8.4e    %4d %4d %4d %4d" % (imagePath, r, v, startX, startY, tW*r, tH*r))


	# cv2.imshow("Image", image)
	# cv2.waitKey(0)