# This is a pseudo code file for Merge Robotics

# This is task D5 - > Introduction to Contours and Distance Calculations

# Last task we looped through images with keyboard control, this time we will complicate life by introducing parts of Task G and H to measure distance from camera to a vision target

# You can find answers to complete this task in the following links 
# -> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html
# -> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contours_begin/py_contours_begin.html#contours-getting-started
# -> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html#contour-area
# -> https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html#a-straight-bounding-rectangle
# -> https://docs.wpilib.org/en/stable/docs/software/vision-processing/introduction/identifying-and-processing-the-targets.html?highlight=distance#measurements

# To help we have comments to prompt how to do this is below

# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

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
arrImageFiles.append('01dinf-pegs-14hiin.jpg')
arrImageFiles.append('02dinf-pegs-14hiin.jpg')
arrImageFiles.append('03dinf-pegs-14hiin.jpg')
arrImageFiles.append('04dinf-pegs-14hiin.jpg')
arrImageFiles.append('05dinf-pegs-14hiin.jpg')
arrImageFiles.append('06dinf-pegs-14hiin.jpg')
arrImageFiles.append('07dinf-pegs-14hiin.jpg')
arrImageFiles.append('08dinf-pegs-14hiin.jpg')
arrImageFiles.append('09dinf-pegs-14hiin.jpg')
arrImageFiles.append('10dinf-pegs-14hiin.jpg')
arrImageFiles.append('11dinf-pegs-14hiin.jpg')
arrImageFiles.append('12dinf-pegs-14hiin.jpg')
arrImageFiles.append('13dinf-pegs-14hiin.jpg')
arrImageFiles.append('14dinf-pegs-14hiin.jpg')
arrImageFiles.append('15dinf-pegs-14hiin.jpg')
arrImageFiles.append('16dinf-pegs-14hiin.jpg')
arrImageFiles.append('17dinf-pegs-14hiin.jpg')
arrImageFiles.append('18dinf-pegs-14hiin.jpg')
arrImageFiles.append('19dinf-pegs-14hiin.jpg')
arrImageFiles.append('20dinf-pegs-14hiin.jpg')

# setup loop
flgExit = False
intCounter = 0
while not(flgExit):

    # load a color image using the string and array
    bgrOriginal = cv2.imread(strPathName + arrImageFiles[intCounter])

    # mask the image to only show yellow or green images
    hsvOriginal = cv2.cvtColor(bgrOriginal, cv2.COLOR_BGR2HSV)
    
    # define a range of from upper to lower in HSV
    arrLowerColor = np.array([colHsvLowerGreen], dtype='int32')
    arrUpperColor = np.array([colHsvUpperGreen], dtype='int32') 
    
    # threshold the HSV image to get only green color
    mskBinary = cv2.inRange(hsvOriginal, arrLowerColor, arrUpperColor)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinary)

    # generate the array of Contours
    contours, hierarchy = cv2.findContours(mskBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort the array of Contours by area
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    print('Found', len(contours), 'contours in this photo!')
    indiv = contours[0]
    print (indiv)

    # draw circle at centroid of target on colour mask, and known distance to target as text
    cv2.drawContours(mskColor, [indiv], 0, colRgbPurple, 3)
    cv2.putText(mskColor, 'Real Dist: ' + str(int(arrImageFiles[intCounter][:2])) + ' ft', (20, 40), font, 0.5, colRgbYellow, 1, cv2.LINE_AA)
    M = cv2.moments(indiv)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(mskColor, (cx,cy), 4, colRgbPurple, -1)

    # indicare the height of the found target, assumed to be largest contour
    ix, iy, iw, ih = cv2.boundingRect(indiv)
    cv2.putText(mskColor, 'Target Height: ' + str(ih) + ' pixels', (20, 60), font, 0.5, colRgbYellow, 1, cv2.LINE_AA)

    # display the colour mask image to screen
    cv2.imshow('This is the Colour mask', mskColor)

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