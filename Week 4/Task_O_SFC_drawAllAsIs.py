# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

# Constants!
# colors for screen information
colBgrOrange = (0, 128, 255)
colRgbPurple = (255, 102, 153)

def drawAllAsIs(bgrOriginal, mskBinary, contours):

    # draw all the contours on the color mask
    cv2.drawContours(bgrOriginal, contours, -1, colBgrOrange, 2)

    # create a full color mask
    # Bitwise-AND binary mask and original image
    mskColor = cv2.bitwise_and(bgrOriginal, bgrOriginal, mask=mskBinary)

    # draw circle at centroid of target on colour mask, and known distance to target as text
    M = cv2.moments(contours[0])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(mskColor, (cx,cy), 4, colRgbPurple, -1)

    # display the colour mask image to screen
    cv2.imshow('This is the Colour mask', mskColor)

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
    ke = drawAllAsIs(bgrTestImage, mskBinary, contours)

    # print user keypress
    print ('ke = ', ke)

    # cleanup and exit
    cv2.destroyAllWindows()
