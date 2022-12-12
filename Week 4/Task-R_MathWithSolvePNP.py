# This is a pseudo code file for Merge Robotics

# This is task R - > Math with Solve PNP function

# On the GIGMM trail we have used some simple math in the past, now let's look 
# at some complex math, or a specific function from OpenCV called SolvePNP

# to get there, lots of learning... but with sample code, here are some links

# https://docs.opencv.org/4.5.0/d9/db7/tutorial_py_table_of_contents_calib3d.html
# https://github.com/ligerbots/VisionServer/blob/master/utils/camera_calibration.py
# https://markhedleyjones.com/storage/checkerboards/Checkerboard-A4-25mm-10x7.pdf
# https://github.com/ligerbots/VisionServer/blob/master/data/calibration/chessboard_9x6.png

# start with Task G code, add some D5 and a little of G and H

# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2
from masking import maskByColor
from Task_R_Camera_Calibrations import *
from Task_R_SolvePNP_Module import *

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
booChooser = True  # True is green and targets at distance, False is orange and cones for now
tupNewImageSize = (640, 480)

# colors for HSV filtering
if booChooser:
    colHsvLowerRange = (50, 100, 100) # green
    colHsvUpperRange = (90, 255, 255) # green
else:
    colHsvLowerRange = (50, 100, 100) # green try 50, 100, 100
    colHsvUpperRange = (90, 255, 255) # green try 90, 255, 255

# fonts for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# 52 is sketchup
camera_matrix, dist_coeffs = load_camera_details(52)

# distance from center to tip in four directions
#diamond_distance = 12.342
#diamond_distance = 10.342
diamond_distance = 9.62

# this is setting up the target for SolvePNP
real_world_coordinates = np.array([
    [-diamond_distance*1.81, 0.0, 0.0],
    [0.0, -diamond_distance, 0.0],
    [+diamond_distance*1.81, 0.0, 0.0],
    [0.0, +diamond_distance, 0.0],
])

# define a string variable for the path to the file
if booChooser:
    strPathName = '2021-irahFourDiamonds/'
else:
    strPathName = '2021-irahTapeTesting/'

# define an array with the names of images 
arrImageFiles = []

# fill an array with the names of images 
if booChooser:
    arrImageFiles.append('fourDiamonds-06f-00d.jpg')
    arrImageFiles.append('fourDiamonds-06f-35d.jpg')
    arrImageFiles.append('fourDiamonds-06f+35d.jpg')
    arrImageFiles.append('fourDiamonds-10f-00d.jpg')
    arrImageFiles.append('fourDiamonds-14f-00d.jpg')
    arrImageFiles.append('fourDiamonds-14f-20d.jpg')
    arrImageFiles.append('fourDiamonds-14f+20d.jpg')    
    arrImageFiles.append('fourDiamonds-18f-00d.jpg')
    arrImageFiles.append('fourDiamonds-20f-10d.jpg')
    arrImageFiles.append('fourDiamonds-20f+10d.jpg')    
    arrImageFiles.append('fourDiamonds-22f-00d.jpg')
    arrImageFiles.append('fourDiamonds-26f-00d.jpg')
else:
    arrImageFiles.append('circleSquare-06f-00d.png')
    arrImageFiles.append('circleSquare-06f-35d.png')
    arrImageFiles.append('circleSquare-06f+35d.png')
    arrImageFiles.append('circleSquare-10f-00d.png')
    arrImageFiles.append('circleSquare-14f-00d.png')
    arrImageFiles.append('circleSquare-14f-20d.png')
    arrImageFiles.append('circleSquare-14f+20d.png')    
    arrImageFiles.append('circleSquare-18f-00d.png')
    arrImageFiles.append('circleSquare-22f-00d.png')

# setup loop
flgExit = False
intCounter = 0
while not(flgExit):

    # print file to 
    print(arrImageFiles[intCounter])

    # load a color image using the string and array
    bgrOriginal = cv2.imread(strPathName + arrImageFiles[intCounter])

    # mask the image to only show yellow or green images
    hsvOriginal = cv2.cvtColor(bgrOriginal, cv2.COLOR_BGR2HSV)
    
    # define a range of from upper to lower in HSV
    arrLowerColor = np.array([colHsvLowerRange])
    arrUpperColor = np.array([colHsvUpperRange])

    # threshold the HSV image to get only green color
    mskBinary = maskByColor(hsvOriginal, arrLowerColor, arrUpperColor, 'kn')

    # optional dialate/erosion to smooth edges and stabilize the centroids, but at cpu cost
    #kernel = np.ones((5,5), np.uint8)       
    #mskBinary = cv2.erode(mskBinary, kernel)
    #mskBinary = cv2.morphologyEx(mskBinary, cv2.MORPH_CLOSE, kernel)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinary)
    mskExcluded = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=cv2.bitwise_not(mskBinary))

    # generate the array of Contours
    contours, hierarchy = cv2.findContours(mskBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort the array of Contours by area
    sortedContours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)[:4]

    # create array to store contours filtered
    diamondContours = []

    # loop though all the contours
    for intCount, indiv in enumerate(sortedContours):

        # calculate the bounding extent
        area = cv2.contourArea(indiv)

        if area == 0:
            continue

        brx, bry, brw, brh = cv2.boundingRect(indiv)
        brextent = area / (brw * brh)
        (arx, ary), (arw, arh), ara = cv2.minAreaRect(indiv)
        arextent = area / (arw * arh)

        #print('arextent', arextent, 'brextent', brextent)

        if arextent > 0.70 and (0.40 < brextent < 0.60): 
            #indiv = cv2.convexHull(indiv) # may improve video stability
            diamondContours.append(indiv)

    # if there are contours found
    if len(diamondContours) == 4:

        print('Found', len(diamondContours), 'diamonds in this photo!')

        # create array to store centroids
        diamondCentroids = []

        # loop though all the contours, store centroid and sorting method
        for intCount, indiv in enumerate(diamondContours):

            # from this tutorial
            # https://docs.opencv.org/4.5.0/dd/d49/tutorial_py_contour_features.html

            # 1 Moments
            M = cv2.moments(indiv)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            diamondCentroids.append([(cx, cy), int(cx*cy)])            

        # sort the four diamnds by the product of their centroid coordinates
        sortedCentroids = sorted(diamondCentroids, key=lambda x: x[1], reverse=False)[:4]

        # draw circle at centroid of target on colour mask, and known distance to target as text
        #cv2.circle(mskColor, (cx,cy), 4, colBgrPurple, -1)

        leftmost = sortedCentroids[0][0]
        rightmost = sortedCentroids[3][0]
        topmost = sortedCentroids[1][0]
        bottommost = sortedCentroids[2][0]

        # draw the extreme points
        cv2.circle(mskColor, leftmost, 4, colBgrGreen, -1)
        cv2.circle(mskColor, rightmost, 4, colBgrRed, -1)
        cv2.circle(mskColor, topmost, 4, colBgrWhite, -1)
        cv2.circle(mskColor, bottommost, 4, colBgrBlue, -1)
 
        # fill found corners with the most data set found in the image
        found_corners = np.array([leftmost, topmost, rightmost, bottommost], dtype="double")

        # use SolvePNP to produce the result vectors
        (success, rotation_vector, translation_vector) = cv2.solvePnP(real_world_coordinates, found_corners, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_AP3P)

        if success:
            inches, angle1, angle2 = compute_output_values(rotation_vector, translation_vector)
            print('Is this correct? -->', inches / 12, angle1, angle2)
        else:
            print('nothing was measured')

    # display the colour mask image to screen
    cv2.imshow('This is Task R', cv2.resize(mskColor, tupNewImageSize))
    #cv2.imshow('This is Task R Excluded', cv2.resize(mskExcluded, tupNewImageSize))

    # wait for user input to move or close
    while(True):
        ke = cv2.waitKeyEx(0)
        #print('you pressed ',ke, intCounter)
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

    # if staying in loop then clean the windows we want to re-use
    cv2.destroyWindow('This is Task G')
    cv2.destroyWindow('This is Task G Excluded')

# cleanup and exit
cv2.destroyAllWindows()



