# This is a pseudo code file for Merge Robotics

# This is task D1 - > Load and Display Images

# Using Python and OpenCV, write a small bit of code to load an image and display it on your screen.

# Recommeded starting points 
#    -> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html

# To help we have comments to prompt how to do this is below

# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

# define a string variable for the path to the file
strPathName = 'Week 1/'
strImageFilename = '2016-stonghold-high-tower-goal.png'

# load a color image using string
bgrOriginal = cv2.imread(strPathName + strImageFilename)

# display the color image to screen
cv2.imshow('This is the window name', bgrOriginal)

# wait for user input to close
cv2.waitKey(0)

# cleanup and exit
cv2.destroyAllWindows()
