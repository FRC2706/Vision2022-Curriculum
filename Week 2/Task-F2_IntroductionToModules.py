# This is a pseudo code file for Merge Robotics

# This is task F2 - > Introduction to Modules

# In task F we found an intersting techinique on the Knoxville github page including a function called 'hsvThreshold'

# You can find their full file here with 'hsvThreshold' embedded as part of it.   
# - https://github.com/Knoxville-FRC-alliance/Vision-2018-Python/blob/master/visionPi.py

# As an experiment let's try this method out by copying task D5 and modifying it to work with their function.
# I understand that the proper Python terms for a function in a separate file is called a modules, so we will
# also use a new folder called modules, a .py file called 'masking.py' as a chooser of sorts, with a sub folder
# for code breakdown called maskers

# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2
from masking import maskByColor

# Constants!
# colors for screen information
colBgrBlue = (255, 0, 0)
colBgrGreen = (0 , 255, 0)
colBgrRed = (0, 0, 255)
colRgbYellow = (0, 255, 255)
colRgbPurple = (255, 102, 153)

# colors for HSV filtering
colHsvLowerGreen = (55, 220, 220)
colHsvUpperGreen = (65, 255, 255)

# fonts for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# define a string variable for the path to the file
strPathName = '2017-pegsAtDistance/'

# define and fill an array with the names of images 
arrImageFiles = []
# arrImageFiles.append('01dinf-pegs-14hiin.jpg')
# arrImageFiles.append('02dinf-pegs-14hiin.jpg')
# arrImageFiles.append('03dinf-pegs-14hiin.jpg')
# arrImageFiles.append('04dinf-pegs-14hiin.jpg')
# arrImageFiles.append('05dinf-pegs-14hiin.jpg')
# arrImageFiles.append('06dinf-pegs-14hiin.jpg')
# arrImageFiles.append('07dinf-pegs-14hiin.jpg')
# arrImageFiles.append('08dinf-pegs-14hiin.jpg')
# arrImageFiles.append('09dinf-pegs-14hiin.jpg')
# arrImageFiles.append('10dinf-pegs-14hiin.jpg')
# arrImageFiles.append('11dinf-pegs-14hiin.jpg')
# arrImageFiles.append('12dinf-pegs-14hiin.jpg')
# arrImageFiles.append('13dinf-pegs-14hiin.jpg')
# arrImageFiles.append('14dinf-pegs-14hiin.jpg')
# arrImageFiles.append('15dinf-pegs-14hiin.jpg')
# arrImageFiles.append('16dinf-pegs-14hiin.jpg')
# arrImageFiles.append('17dinf-pegs-14hiin.jpg')
# arrImageFiles.append('18dinf-pegs-14hiin.jpg')
# arrImageFiles.append('19dinf-pegs-14hiin.jpg')
# arrImageFiles.append('20dinf-pegs-14hiin.jpg')

if True:
    strPathName = '2018-PowerUp-Problems/'

    arrImageFiles = []
    arrImageFiles.append('test-01.jpg')
    arrImageFiles.append('test-02.jpg')
    arrImageFiles.append('test-03.jpg')
    arrImageFiles.append('test-04.jpg')
    arrImageFiles.append('test-05.jpg')

    colHsvLowerGreen = (30, 220, 100)
    colHsvUpperGreen = (40, 255, 255)

# setup loop
flgExit = False
intCounter = 0
while not(flgExit):

    # load a color image using the string and array
    bgrOriginal = cv2.imread(strPathName + arrImageFiles[intCounter])

    # mask the image to only show yellow or green images
    hsvOriginal = cv2.cvtColor(bgrOriginal, cv2.COLOR_BGR2HSV)
    
    # define a range of from upper to lower in HSV
    arrLowerColor = np.array([colHsvLowerGreen])
    arrUpperColor = np.array([colHsvUpperGreen])
    
    # threshold the HSV image to get only green color
    mskBinaryIr = maskByColor(hsvOriginal, arrLowerColor, arrUpperColor, 'ir')
    mskBinaryKn = maskByColor(hsvOriginal, arrLowerColor, arrUpperColor, 'kn')

    # display the binary masks image to screen
    cv2.imshow('This is the Binary mask - InRange', mskBinaryIr)
    cv2.imshow('This is the Binary mask - Knoxville', mskBinaryKn)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColorIr = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinaryIr)
    mskColorKn = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinaryKn)

    # generate the array of Contours
    contours, hierarchy = cv2.findContours(mskBinaryKn, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort the array of Contours by area
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    print('Found', len(contours), 'contours in this photo!')
    indiv = contours[0]
    #print (indiv)

    # draw circle at centroid of target on colour mask, and known distance to target as text
    cv2.drawContours(mskColorKn, [indiv], 0, colRgbPurple, 3)
    #cv2.putText(mskColorKn, 'Real Dist: ' + str(int(arrImageFiles[intCounter][:2])) + ' ft', (20, 40), font, 0.5, colRgbYellow, 1, cv2.LINE_AA)
    M = cv2.moments(indiv)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(mskColorKn, (cx,cy), 4, colRgbPurple, -1)

    # indicare the height of the found target, assumed to be largest contour
    ix, iy, iw, ih = cv2.boundingRect(indiv)
    cv2.putText(mskColorKn, 'Target Height: ' + str(ih) + ' pixels', (20, 60), font, 0.5, colRgbYellow, 1, cv2.LINE_AA)

    # display the colour mask image to screen
    cv2.imshow('This is the Colour mask from InRange', mskColorIr)
    cv2.imshow('This is the Colour mask from Knoxville', mskColorKn)

    # wait for user input to move or close
    while(True):
        ke = cv2.waitKeyEx(0)
        if ke == 113 or ke == 27:
            flgExit = True
            break
        if ke == 105 or ke == 2490368:
            intCounter = intCounter - 1
            if intCounter < 0: 
                intCounter = len(arrImageFiles) - 1
            break
        if ke == 109 or ke == 2621440:
            intCounter = intCounter + 1
            if intCounter > len(arrImageFiles) - 1:
                intCounter = 0
            break

# cleanup and exit
cv2.destroyAllWindows()