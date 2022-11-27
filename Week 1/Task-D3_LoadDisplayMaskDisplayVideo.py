# This is a pseudo code file for Merge Robotics

# This is task D3 - > Load Display Mask Display Video

# Using Python and OpenCV, write a small bit of code to load an image from a webcam and display it on your screen.  Then mask it to green or yellow and display that.  Keep looping to make a video.  Find some green or yellow object in your house to practice on.

# Recommeded starting points -> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html

# To help we have comments to prompt how to do this is below

# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

# NEW - Constants for various purposes...
# for Camera number, when using more than one, generally, 0 is my laptop camera, 1 is first usb webcam found
intCameraNumber = 0

# colors for screen information
colRgbBlue = (255, 0, 0)
colRgbGreen = (0 , 255, 0)
colRgbRed = (0, 0, 255)

# choose Lower and Upper colors, and exposures based on Camera selected above
if intCameraNumber == 1:
    colHsvLowerGreen = (45, 30, 127)
    colHsvUpperGreen = (85, 255, 255)
elif intCameraNumber == 0:
    colHsvLowerGreen = (60, 60, 70)
    colHsvUpperGreen = (100, 255, 255)

# define the camera
# CAP_DSHOW tells OpenCV / Windows to use the DirectShow API
# 0 is my laptop camera, 1 is first usb webcam found
cap = cv2.VideoCapture(intCameraNumber + cv2.CAP_DSHOW)

if intCameraNumber == 1:
    pass
elif intCameraNumber == 0:
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) # turns off auto exposure
    cap.set(cv2.CAP_PROP_EXPOSURE, -8) # turns exposure to seconds based on power of 2, so negative is a small duration
    
# setup loop
while(True):

    # load a color image from camera
    # Capture frame-by-frame
    ret, bgrOriginal = cap.read()

    # display the color image to screen
    cv2.imshow('This is the original image', bgrOriginal)

    # mask the image to only show yellow or green images
    # Convert RGB(BGR) to HSV
    hsvOriginal = cv2.cvtColor(bgrOriginal, cv2.COLOR_BGR2HSV)

    # define a range of from upper to lower in HSV
    arrLowerColor = np.array([colHsvLowerGreen])
    arrUpperColor = np.array([colHsvUpperGreen]) 

    # threshold the HSV image to get only green color
    mskBinary = cv2.inRange(hsvOriginal, arrLowerColor, arrUpperColor)

    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinary)

    # display the masked images to screen
    cv2.imshow('This is the Binary mask', mskBinary)
    cv2.imshow('This is the Colour mask', mskColor)

    # check for user input to exit loop and if not return to top of loop
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27:
        break

# cleanup and exit
cap.release()
cv2.destroyAllWindows()
