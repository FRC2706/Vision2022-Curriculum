# This is a pseudo code file for Merge Robotics

# This is task H - > OpenCV "Contour Calculations."  Not sure if it is clear by now, 
# but OpenCV can do a lot of things, we need to understand what it offers to complete 
# our vision code.  For a given single contour, (meaning it was imaged and masked and 
# converted to a coordinate array), you need to be able to use a number of OpenCV functions.
# Please experiment with the following, easiest is to simply draw them back to a blank image
# or on top of original.

# --> moments, contour area, contour perimeter, contour approximation, bounding rectangles, 
# minimum enclosing circle, fitting elipse, fitting line, etc.

# useful links
# https://docs.opencv.org/4.5.0/d1/d32/tutorial_py_contour_properties.html

# 1 Aspect Ratio
# 2 Extent
# 3 Solidity
# 4 Equivalent Diameter
# 5 Orientation
# 6 Mask and Pixel Points
# 7 Maximum Value, Minimum Value and their locations
# 8 Mean Color or Mean Intensity
# 9 Extreme Points

# most of this code was taken from Task F2

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
colBgrYellow = (0, 255, 255)
colBgrPurple = (255, 102, 153)

colBgrWhite = (255, 255, 255)
colBgrBlack = (0, 0, 0)
colBgrGrey = (160, 160, 160)
colBgrOrange = (0, 128, 255)
colBgrTeal = (128, 128, 0)

colBgrApple = (0, 191, 17)
colBgrPacific = (193, 161,0)
colBgrAtlantis = (0, 217, 105)
colBgrCerise = (120, 0, 216)
colBgrJewel = (64, 109, 0)
colBgrFruit = (64, 155, 64)

# flags and multipliers for decision making
booChooser = True  # True is yellow and worlds, False is green and targets at distance
tupNewImageSize = (640, 480)

# colors for HSV filtering
if booChooser:
    colHsvLowerRange = (24, 100, 178) # yellow
    colHsvUpperRange = (36, 255, 255) # yellow
else:
    colHsvLowerRange = (50, 100, 100) # green 
    colHsvUpperRange = (90, 255, 255) # green 

# fonts for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# define a string variable for the path to the file
if booChooser:
    strPathName = '2018-MergeAtWorlds/'
else:
    strPathName = '2021-targetAtDistances/'

# define an array with the names of images 
arrImageFiles = []

# fill an array with the names of images 
if booChooser:
    arrImageFiles.append('03320_raw.png')
    arrImageFiles.append('03952_raw.png')
    arrImageFiles.append('04547_raw.png')
    arrImageFiles.append('04615_raw.png')
    arrImageFiles.append('04664_raw.png')
    arrImageFiles.append('04766_raw.png')
    arrImageFiles.append('07040_raw.png')
else:
    arrImageFiles.append('2021-01-09-093425-03.png')
    arrImageFiles.append('2021-01-09-093550-04.png')
    arrImageFiles.append('2021-01-09-093638-05.png')
    arrImageFiles.append('2021-01-09-093711-06.png')
    arrImageFiles.append('2021-01-09-093740-07.png')
    arrImageFiles.append('2021-01-09-093821-08.png')
    arrImageFiles.append('2021-01-09-093902-09.png')
    arrImageFiles.append('2021-01-09-094009-10.png')
    arrImageFiles.append('2021-01-09-094029-11.png')
    arrImageFiles.append('2021-02-16-203307-12.png')

# setup loop
flgExit = False
intCounter = len(arrImageFiles) - 1

# begin loop
while not(flgExit):

    # a blank space at start of each file
    print() 

    # print file to 
    print('The file shown now is', arrImageFiles[intCounter])

    # load a color image using the string and array
    bgrOriginal = cv2.imread(strPathName + arrImageFiles[intCounter])

    # mask the image to only show yellow or green images
    hsvOriginal = cv2.cvtColor(bgrOriginal, cv2.COLOR_BGR2HSV)
    
    # define a range of from upper to lower in HSV
    arrLowerColor = np.array([colHsvLowerRange])
    arrUpperColor = np.array([colHsvUpperRange])

    # threshold the HSV image to get only green color
    mskBinary = maskByColor(hsvOriginal, arrLowerColor, arrUpperColor, 'ir')

    # display the binary masks image to screen
    #cv2.imshow('This is the Binary mask - Knoxville', mskBinary)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinary)

    # generate the array of Contours
    contours, hierarchy = cv2.findContours(mskBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print('Found', len(contours), 'contours in this photo!')
    
    # sort the array of Contours by area
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)[:8]

    # draw the largets 8 contours on the color mask
    print('The largerst 8 contours are outlined in orange')
    cv2.drawContours(mskColor, contours, -1, colBgrOrange, 2)

    # if there are no contours found
    if contours:
        indiv = contours[0]

        # draw the indiv contour on the color mask
        print('The largest contour is outlined in purple')
        cv2.drawContours(mskColor, [indiv], 0, colBgrPurple, 5)

        # from this tutorial, do all the functions
        # https://docs.opencv.org/4.5.0/d1/d32/tutorial_py_contour_properties.html

        # these task H functions need some of the math from Task G
        area = cv2.contourArea(indiv)
        hull = cv2.convexHull(indiv)
        brx, bry, brw, brh = cv2.boundingRect(indiv)
        rect = cv2.minAreaRect(indiv)
        ellipse = cv2.fitEllipse(indiv)

        # 1 Aspect Ratio, note can do bounding rectangle or minArea rectangle
        print('The bounding Aspect Ratio is', '{:.2f}'.format(brw / brh))

        # 2 Extent, note can do bounding or minArea rectangle
        print('The bounding Extent is', '{:.2f}'.format(area / (brw * brh)))

        # 3 Solidity
        hull_area = cv2.contourArea(hull)
        print('The solidity of the contour is', '{:.2f}'.format(area / hull_area))

        # 4 Equivalent Diameter
        pass

        # 5 Orientation
        pass

        # 6 Mask and Pixel Points
        pass

        # 7 Maximum Value, Minimum Value and their locations
        pass

        # 8 Mean Color or Mean Intensity
        pass

        # 9 Extreme Points  
        leftmost = tuple(indiv[indiv[:,:,0].argmin()][0])
        rightmost = tuple(indiv[indiv[:,:,0].argmax()][0])
        topmost = tuple(indiv[indiv[:,:,1].argmin()][0])
        bottommost = tuple(indiv[indiv[:,:,1].argmax()][0])

        # draw bounding rectangle
        print('The bounding rectangle is outline in white')
        cv2.rectangle(mskColor,(brx,bry),(brx+brw,bry+brh),colBgrWhite,1)

        # draw the hull on the color mask
        print('The hull is outlined in yellow')
        cv2.drawContours(mskColor, [hull], 0, colBgrYellow, 2)

        # draw the equivalent circle diameter

        # draw the extreme points
        cv2.circle(mskColor, leftmost, 4, colBgrGreen, -1)
        cv2.circle(mskColor, rightmost, 4, colBgrRed, -1)
        cv2.circle(mskColor, topmost, 4, colBgrWhite, -1)
        cv2.circle(mskColor, bottommost, 4, colBgrBlue, -1)

    # display the colour mask image to screen
    cv2.imshow('This is Task H', cv2.resize(mskColor, tupNewImageSize))

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
