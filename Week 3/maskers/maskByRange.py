import cv2

def maskByRange(hsvImage, colHsvLower, colHsvUpper):
    return cv2.inRange(hsvImage, colHsvLower, colHsvUpper)