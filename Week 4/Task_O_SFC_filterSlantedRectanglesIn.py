# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

# Constants!
# colors for screen information
colBgrOrange = (0, 128, 255)
colRgbPurple = (255, 102, 153)
colBgrBlue = (255, 0, 0)
colBgrGreen = (0 , 255, 0)
colBgrRed = (0, 0, 255)
colBgrYellow = (0, 255, 255)
colBgrPurple = (255, 102, 153)
colBgrWhite = (255, 255, 255)

def filterSlantedRectanglesIn(bgrImage, mskImage, contours, cv2v):

    # the _ is a waste bin for data from the shape property, we don't need
    (height, width, _) = bgrImage.shape
    
    # create array to store contours filtered
    squareContours = []

    intCounter = 0
    # loop though all the contours
    for indiv in contours:

        # calculate the bounding extent
        area = cv2.contourArea(indiv)
        brx, bry, brw, brh = cv2.boundingRect(indiv)
        brextent = area / (brw * brh)
        rect = cv2.minAreaRect(indiv)
        rect = fixMinAreaRect(rect, cv2v)
        (arx, ary), (arw, arh), ara = rect
        arextent = area / (arw * arh)

        if (18 > abs(ara) > 8): 
            squareContours.append(indiv)
            #print(f'contour area={area}, width={brw}, height={brh}, brarea={brw*brh}')
            #print('indiv=', intCounter, 'brextent=', brextent)
            #print(f'contour area={area}, width={arw}, height={arh}, brarea={arw*arh}')
            #print('indiv=', intCounter, 'arextent=', arextent)

        intCounter += 1

    # draw the outline of the filtered contours on the color mask
    cv2.drawContours(bgrImage, squareContours, -1, colBgrOrange, 2)

    # create a new mask with only the desired contours
    mskBinarySquares = np.zeros(shape=[height, width, 1], dtype=np.uint8)
    cv2.drawContours(mskBinarySquares, squareContours, -1, 255, -1)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrImage, bgrImage, mask=mskBinarySquares)

    if squareContours:

        # sort contours by area decreasing
        #sortedContours = sorted(squareContours, key=lambda x: cv2.contourArea(x), reverse=True)

        # sort contours by area increasing
        #sortedContours = sorted(squareContours, key=lambda x: cv2.contourArea(x), reverse=True)

        # sort contours by leftmost point of contour
        sortedContours = sorted(squareContours, key=lambda x: tuple(x[x[:,:,0].argmin()][0])[0], reverse=False)
    
        indiv = sortedContours[0]

        # draw circle at centroid of target on colour mask, and known distance to target as text
        M = cv2.moments(indiv)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(mskColor, (cx,cy), 4, colRgbPurple, -1)

        # 9 Extreme Points  
        leftmost = tuple(indiv[indiv[:,:,0].argmin()][0])
        rightmost = tuple(indiv[indiv[:,:,0].argmax()][0])
        topmost = tuple(indiv[indiv[:,:,1].argmin()][0])
        bottommost = tuple(indiv[indiv[:,:,1].argmax()][0])

        # draw the extreme points
        cv2.circle(mskColor, leftmost, 4, colBgrGreen, -1)
        cv2.circle(mskColor, rightmost, 4, colBgrRed, -1)
        cv2.circle(mskColor, topmost, 4, colBgrWhite, -1)
        cv2.circle(mskColor, bottommost, 4, colBgrBlue, -1)

    # display the colour mask image to screen
    cv2.imshow('Filtered rectangles by angle colour mask', mskColor)

    # wait for user input to close
    while(True):
        ke = cv2.waitKey(0) & 0xFF
        if ke == ord('q') or ke == 27:
            break
        if 105 or ke == 2490368: # ke == ord('i') or
            break
        if 109 or ke == 2621440:
            break

    # cleanup and exit
    #cv2.destroyAllWindows()

    return ke

# Deal with odd behavior of cv3 vs cv4 and MinARect in OPenCV
def fixMinAreaRect(rectangle, cv2v):

    # cv2 version 3 and cv2 version 4 return the width, height and angle in minAreaRect differently.
    # this function take the reactangle and OpenCV version as input, and adjusts the angle so that it
    # is between -90 deg to the left and +90 deg to the right, with zero in the middle.  The width
    # and height are always with respect to the shape, so a tall rect on it's side is still tall.

    ((xmr, ymr), (wmr, hmr), amr) = rectangle

    if cv2v[0] == '3':
        if wmr > hmr:
            wmr, hmr = hmr, wmr
            amr = (90 + amr)
    elif cv2v[0] == '4':
        if wmr > hmr:
            wmr, hmr = hmr, wmr
            amr = - (90 - amr)

    return ((xmr, ymr), (wmr, hmr), amr)

if __name__ == "__main__":

    import sys

    # Print python version
    print('\n')
    print('Python version', sys.version, '\n')

    # Print version string
    cv2Version = '{0}'.format(cv2.__version__)
    print('OpenCV version', '{0}'.format(cv2.__version__), '\n')

    # setup image counter
    imageCounter = 0

    # create empty bgr image for the test
    bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)

    # draw a green rectangle on the test image
    bgrTestImage = cv2.rectangle(bgrTestImage,(100,80),(130,200),(0,255,0),-1)

    # draw a left green tape on the test image
    pts = np.array([[59,51],[75,56],[62,103],[46,98]], np.int32)
    bgrTestImage = cv2.drawContours(bgrTestImage,[pts],0,(0,255,0), -1)

    # draw a right green tape on the test image
    pts = np.array([[147,56],[163,51],[176,98],[160,102]], np.int32)
    bgrTestImage = cv2.drawContours(bgrTestImage,[pts],0,(0,255,0), -1)

    # draw a second left green tape on the test image
    pts = np.array([[259,51],[275,56],[262,103],[246,98]], np.int32)
    bgrTestImage = cv2.drawContours(bgrTestImage,[pts],0,(0,255,0), -1)

    # display the test image to verify it visually
    cv2.imshow('This is the test image', bgrTestImage)

    # convert image to hsv from bgr
    hsvTestImage = cv2.cvtColor(bgrTestImage, cv2.COLOR_BGR2HSV)

    # using inrange from opencv make mask
    mskBinary = cv2.inRange(hsvTestImage,  (55, 220, 220), (65, 255, 255),)

    # generate the array of Contours
    contours, hierarchy = cv2.findContours(mskBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print('Found', len(contours), 'contours in this photo!')

    # pass test image, binary mask and cotours to function to display all as is
    ke = filterSlantedRectanglesIn(bgrTestImage, mskBinary, contours, cv2Version)

    indiv = contours[0]

    # print user keypress
    print ('ke = ', ke)

    # cleanup and exit
    cv2.destroyAllWindows()
