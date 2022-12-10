# This is a pseudo code file for Merge Robotics

# This is task J2 - > Measure Time of OpenCV Functions.  This is a series of tasks we are going to 
# learn how to create our own function, and test the speed of different ways of writing the
# function.  The reason for this is actually to simultaneously make our code easier to read
# and perform better.  Both re-usability and speed make the code powerful for future use as well.

# Task J2 will introduce a comparison of the two maskers we have looked at in the modules folder.

# note most of this is a copy paste from Task J1, some from Task G and Task D5

# imports
import numpy as np
import cv2
import timeit
from masking import maskByColor

# constants
# colors for screen information
colBgrYellow = (0, 255, 255)

# colors for HSV filtering
colHsvLowerGreen = (55, 220, 220)
colHsvUpperGreen = (65, 255, 255)
arrLowerColor = np.array([colHsvLowerGreen])
arrUpperColor = np.array([colHsvUpperGreen]) 

# NEW - we are going to define new functions here
def irx2500():
    SETUP_CODE = '''
import numpy as np
import cv2
from masking import maskByColor
colHsvLowerGreen = (55, 220, 220)
colHsvUpperGreen = (65, 255, 255)
arrLowerColor = np.array([colHsvLowerGreen])
arrUpperColor = np.array([colHsvUpperGreen]) 
bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)
bgrTestImage = cv2.rectangle(bgrTestImage,(130,20),(160,140),(0,255,0),-1)
hsvTestImage = cv2.cvtColor(bgrTestImage, cv2.COLOR_BGR2HSV)
'''
    TEST_CODE = '''
mskBinaryIR = maskByColor(hsvTestImage, arrLowerColor, arrUpperColor, 'ir')
'''
    timesIR = timeit.repeat(setup = SETUP_CODE, stmt = TEST_CODE, repeat = 3, number = 2500)
    print('in range time: ', '{:.2f}'.format(min(timesIR)))
    return timesIR

def knx2500():
    SETUP_CODE = '''
import numpy as np
import cv2
from masking import maskByColor
colHsvLowerGreen = (55, 220, 220)
colHsvUpperGreen = (65, 255, 255)
arrLowerColor = colHsvUpperGreen
arrUpperColor = colHsvUpperGreen 
arrLowerColor = np.array([colHsvLowerGreen])
arrUpperColor = np.array([colHsvUpperGreen]) 
bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)
bgrTestImage = cv2.rectangle(bgrTestImage,(130,20),(160,140),(0,255,0),-1)
hsvTestImage = cv2.cvtColor(bgrTestImage, cv2.COLOR_BGR2HSV)
'''
    TEST_CODE = '''
mskBinaryKN = maskByColor(hsvTestImage, arrLowerColor, arrUpperColor, 'kn')
'''
    times = timeit.repeat(setup = SETUP_CODE, stmt = TEST_CODE, repeat = 3, number = 2500)
    print('knoxville time: ', '{:.2f}'.format(min(times)))	

# -=-=-=-=-=-=-=-=-=-
# NEW - This is the start of the main code for this file
# -=-=-=-=-=-=-=-=-=-

# create empty bgr image for the test
bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)

# draw a green rectangle on the test image
bgrTestImage = cv2.rectangle(bgrTestImage,(130,20),(160,140),(0,255,0),-1)

# convert image to hsv from bgr
hsvTestImage = cv2.cvtColor(bgrTestImage, cv2.COLOR_BGR2HSV)

# using 'ir' from opencv time how long it takes to make 1,000 masks
mskBinaryIR = maskByColor(hsvTestImage, arrLowerColor, arrUpperColor, 'ir')
timesIR = irx2500()

# using 'kn' from the Knoxville X time how long it takes to make 1,000 masks
mskBinaryKN = maskByColor(hsvTestImage, arrLowerColor, arrUpperColor, 'kn')
timesKN = knx2500()

# write the average time to the images


# display the test image to verify it visually
cv2.imshow('This is the test', bgrTestImage)

# display the two masks to verify it visually
cv2.imshow('This is the InRange mask', mskBinaryIR)
cv2.imshow('This is the Knoxville mask', mskBinaryKN)

# wait for user input to close
cv2.waitKey(0)

# cleanup and exit
cv2.destroyAllWindows()

