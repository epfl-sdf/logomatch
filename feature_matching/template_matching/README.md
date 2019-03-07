This work is based on the [this](https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/) post.

The idea is to use `cv2.matchTemplate` on many different image sizes.
What is strange is that it seams to quite correctly spot the logo but the output
_score_ does not allow to discriminate between good and bad matches.
I have tried to display the difference image (either the one from `cv2.matchTemplate`, or one recomputed from the original cropped image and the good matches seam to have more white areas and hence should be measurable. Simple norm (average grey level) seam to not work properly.
