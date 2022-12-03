# https://github.com/Knoxville-FRC-alliance/Vision-2018-Python/blob/master/visionPi.py

import numpy as np
import cv2

def hsvThreshold(img, hueMin, hueMax, satMin, satMax, valMin, valMax):

    # hue, sat, val = cv2.split(img)
    hue = img[:,:,0]
    sat = img[:,:,1]
    val = img[:,:,2]

    hueBin = np.zeros(hue.shape, dtype=np.uint8)
    satBin = np.zeros(sat.shape, dtype=np.uint8)
    valBin = np.zeros(val.shape, dtype=np.uint8)

    hueBin = cv2.inRange(hue, hueMin, hueMax)
    satBin = cv2.inRange(sat, satMin, satMax)
    valBin = cv2.inRange(val, valMin, valMax)

    bin = np.copy(hueBin)
    cv2.bitwise_and(satBin, bin, bin)
    cv2.bitwise_and(valBin, bin, bin)
    
    return bin