# This is a pseudo code file for Merge Robotics

# This is task G - > Find Contours.  This is a seemingly simple command. But is where the real math begins.  
# The command basically converts the masked image into arrays of coordinates that we do math on.  Make sure
# you can do this in your code.  You need to end up with a set of contours!  If you print them to the console
# you will see pages and pages of coordinates go by.  Do that at least once.

# useful links
# https://docs.opencv.org/4.5.0/d4/d73/tutorial_py_contours_begin.html

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
    colHsvLowerRange = (0, 100, 100) # green ## BC put back to green
    colHsvUpperRange = (8, 255, 255) # green 

# fonts for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

# define a string variable for the path to the file
if booChooser:
    strPathName = '2018-MergeAtWorlds/'
else:
    strPathName = '2021-conesAsMarkers/' ## BC put back to tape not cones

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
elif False:
    arrImageFiles.append('2021-01-09-093425-03.png')  ## BC put back tape
    arrImageFiles.append('2021-01-09-093550-04.png')
    arrImageFiles.append('2021-01-09-093638-05.png')
    arrImageFiles.append('2021-01-09-093711-06.png')
    arrImageFiles.append('2021-01-09-093740-07.png')
    arrImageFiles.append('2021-01-09-093821-08.png')
    arrImageFiles.append('2021-01-09-093902-09.png')
    arrImageFiles.append('2021-01-09-094009-10.png')
    arrImageFiles.append('2021-01-09-094029-11.png')

else: 
    arrImageFiles.append('pi_cam_test.jpg')
    arrImageFiles.append('marker-01.jpg')

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

    # display the binary masks image to screen
    #cv2.imshow('This is the Binary mask - Knoxville', mskBinary)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinary)
    mskExcluded = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=cv2.bitwise_not(mskBinary))

    # generate the array of Contours
    contours, hierarchy = cv2.findContours(mskBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sort the array of Contours by area
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    print('Found', len(contours), 'contours in this photo!')

    # if there are no contours found
    if contours:
        indiv = contours[0]

        # draw the indiv contour on the color mask
        cv2.drawContours(mskColor, [indiv], 0, colBgrPurple, 3)

        # from this tutorial, do all the functions
        # https://docs.opencv.org/4.5.0/dd/d49/tutorial_py_contour_features.html

        # 2 Area
        area = cv2.contourArea(indiv)

        if area > 1:
            # 1 Moments
            M = cv2.moments(indiv)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            # 3 Permiter
            perimeter = cv2.arcLength(indiv,True)

            # 4 Approx
            epsilon = 0.1*cv2.arcLength(indiv,True)
            approx = cv2.approxPolyDP(indiv,epsilon,True)

            # 5 Convex Hull
            hull = cv2.convexHull(indiv)

            # 6 Convexity
            convflag = cv2.isContourConvex(indiv)

            # 7a Bounding Rectangle
            brx, bry, brw, brh = cv2.boundingRect(indiv)

            # 7b Minimum Area Recctange
            rect = cv2.minAreaRect(indiv)

            # 8 Minimum Enclosing Circle
            (mecx, mecy), radius = cv2.minEnclosingCircle(indiv)
            
            # 9 Fit Elipse
            ellipse = cv2.fitEllipse(indiv)

            # 10 Fit Line
            [vx,vy,flx,fly] = cv2.fitLine(indiv, cv2.DIST_L2,0,0.01,0.01)
            print(vx,vy,flx,fly)

            # draw circle at centroid of target on colour mask, and known distance to target as text
            cv2.circle(mskColor, (cx,cy), 4, colBgrPurple, -1)

            # draw bounding rectangle
            cv2.rectangle(mskColor,(brx,bry),(brx+brw,bry+brh),colBgrOrange,2)

            # draw min area recatangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(mskColor,[box],0,colBgrBlue,2)

            # draw the min eclosing circle
            center = (int(mecx),int(mecy))
            radius = int(radius)
            cv2.circle(mskColor,center,radius,colBgrCerise,2)

            # draw the ellipse
            cv2.ellipse(mskColor,ellipse,colBgrGrey,2)

            # display fit line
            rows, cols = hsvOriginal.shape[:2]
            lefty = int((-flx*vy/vx) + fly)
            righty = int(((cols-flx)*vy/vx)+fly)
            print(lefty,righty)
            print((cols-1,righty),(0,lefty))
            cv2.line(mskBinary,(cols-1,righty),(0,lefty),colBgrWhite,2)

    # display the colour mask image to screen
    cv2.imshow('This is Task G', cv2.resize(mskColor, tupNewImageSize))
    cv2.imshow('This is Task G Excluded', cv2.resize(mskExcluded, tupNewImageSize))

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








