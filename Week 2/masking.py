import numpy as np
import cv2

from maskers.maskByRange import maskByRange
from maskers.maskByKnoxville import hsvThreshold

def maskByColor(hsvImage, LowColor, HighColor, Method):

    if Method == 'ir':
        mskToReturn = maskByRange(hsvImage, LowColor, HighColor)

    elif Method == 'kn':
        # LowColor = LowColor[0]
        # hueMin, satMin, valMin = LowColor[0], LowColor[1], LowColor[2]
        # HighColor = HighColor[0]
        # hueMax, satMax, valMax = HighColor[0], HighColor[1], HighColor[2]
        if isinstance(LowColor,np.ndarray):
            #print('isndarry')
            LowColor = LowColor[0]
            #print(LowColor[0], LowColor[1], LowColor[2])
            hueMin, satMin, valMin = LowColor[0], LowColor[1], LowColor[2]
            #print(hueMin, satMin, valMin)
            HighColor = HighColor[0]
            hueMax, satMax, valMax = HighColor[0], HighColor[1], HighColor[2]
        else:
            #print('notndarray')
            print(LowColor, type(LowColor))
            if isinstance(LowColor,tuple):
                #print('tuple')
                (hueMin, satMin, valMin) = LowColor
                (hueMax, satMax, valMax) = HighColor
            else:
                #print('list')
                LowColor = LowColor[0]
                hueMin, satMin, valMin = LowColor[0], LowColor[1], LowColor[2]
                HighColor = HighColor[0]
                hueMax, satMax, valMax = HighColor[0], HighColor[1], HighColor[2]

        mskToReturn = hsvThreshold(hsvImage, int(hueMin), int(hueMax), int(satMin), int(satMax), int(valMin), int(valMax))

    elif Method == '':
        pass

    else:
        print('No valid method of maskByColor passed to function')
        mskToReturn = None

    return mskToReturn

if __name__ == "__main__":

    # create empty bgr image for the test
    bgrTestImage = np.zeros(shape=[240, 320, 3], dtype=np.uint8)

    # draw a green rectangle on the test image
    bgrTestImage = cv2.rectangle(bgrTestImage,(130,20),(160,140),(0,255,0),-1)

    # display the test image to verify it visually
    cv2.imshow('This is the test', bgrTestImage)

    # convert image to hsv from bgr
    hsvTestImage = cv2.cvtColor(bgrTestImage, cv2.COLOR_BGR2HSV)

    # using inrange from opencv make mask
    mskBinaryIR = maskByColor(hsvTestImage,  ((55, 220, 220)), ((65, 255, 255)), 'ir')
    mskBinaryKN = maskByColor(hsvTestImage,  ((55, 220, 220)), ((65, 255, 255)), 'kn')

    # display the mask to verify it visually
    cv2.imshow('This is the In Range mask', mskBinaryIR)
    cv2.imshow('This is the Knoxville mask', mskBinaryKN)

    # wait for user input to close
    cv2.waitKey(0)

    # cleanup and exit
    cv2.destroyAllWindows()