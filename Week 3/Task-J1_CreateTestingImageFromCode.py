# This is a pseudo code file for Merge Robotics

# This is task J - > Create Testing Image from Code. With a series of tasks we are going to 
# learn how to create our or function, sometimes called a method for our code.  The reason
# for this is actually to simultaneously make our code easier to read and use, but more powerful
# for future use as well

# imports
import numpy as np
import cv2

# constants
colHsvLowerGreen = (55, 220, 220)
colHsvUpperGreen = (65, 255, 255)
arrLowerColor = np.array([colHsvLowerGreen])
arrUpperColor = np.array([colHsvUpperGreen]) 

# create empty bgr image for the test
bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)

# draw a green rectangle on the test image
bgrTestImage = cv2.rectangle(bgrTestImage,(130,20),(160,140),(0,255,0),-1)

# display the test image to verify it visually
cv2.imshow('This is the test', bgrTestImage)

# convert image to hsv from bgr
hsvTestImage = cv2.cvtColor(bgrTestImage, cv2.COLOR_BGR2HSV)

# using inrange from opencv make mask
mskBinary = cv2.inRange(hsvTestImage, arrLowerColor, arrUpperColor)

# display the mask to verify it visually
cv2.imshow('This is the mask', mskBinary)

# wait for user input to close
cv2.waitKey(0)

# cleanup and exit
cv2.destroyAllWindows()