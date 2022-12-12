# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

# Constants!
# colors for screen information
colBgrOrange = (0, 128, 255)
colRgbPurple = (255, 102, 153)

def filterBoundedSquaresIn(bgrImage, mskImage, contours):

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

        #print(f'contour area={area}, width={brw}, height={brh}, brarea={brw*brh}')
        #print('indiv=', intCounter, 'brextent=', brextent)
        if brextent > 0.85: 
            squareContours.append(indiv)

        intCounter += 1

    # draw the outline of the filtered contours on the color mask
    cv2.drawContours(bgrImage, squareContours, -1, colBgrOrange, 2)

    # create a new mask with only the desired contours
    mskBinarySquares = np.zeros(shape=[height, width, 1], dtype=np.uint8)
    cv2.drawContours(mskBinarySquares, squareContours, -1, 255, -1)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrImage, bgrImage, mask=mskBinarySquares)

    # draw circle at centroid of target on colour mask, and known distance to target as text
    M = cv2.moments(squareContours[0])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(mskColor, (cx,cy), 4, colRgbPurple, -1)

    # display the colour mask image to screen
    cv2.imshow('Filtered by bounding extent colour mask', mskColor)

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

if __name__ == "__main__":

    # setup image counter
    imageCounter = 0

    # create empty bgr image for the test
    bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)

    # draw a green rectangle on the test image
    bgrTestImage = cv2.rectangle(bgrTestImage,(130,20),(160,140),(0,255,0),-1)

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
    ke = filterBoundedSquaresIn(bgrTestImage, mskBinary, contours)

    # print user keypress
    print ('ke = ', ke)

    # cleanup and exit
    cv2.destroyAllWindows()
