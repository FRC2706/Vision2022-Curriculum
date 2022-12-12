from pathlib import PosixPath
import numpy as np
import cv2

from pupil_apriltags import Detector

# define a string variable for the path to the file
strPathName = 'apriltagsImages/'
strImageFilename = 'tagsampler.png'

# load a color image using string
bgrOriginal = cv2.imread(strPathName + strImageFilename, cv2.IMREAD_GRAYSCALE)

cv2.imshow('This is the window name', bgrOriginal)

at_detector = Detector(
   families="tag16h5",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0,
   #Note: searchpath is not necessary, since the apriltag lib is installed.
 #  searchpath=(("C:/Users/Wei20/AppData/Local/Programs/Python/Python311/Lib/site-packages/pupil_apriltags/lib"),)
   )

print("img.shape = ", bgrOriginal.shape)

return_info = at_detector.detect(bgrOriginal)
print("return_info " )
print(*return_info, sep=", ")


# wait for user input to close
cv2.waitKey(0)

# cleanup and exit
cv2.destroyAllWindows()