# Imports!
# Python - import modules of code as required (OpenCV here)
import numpy as np
import cv2

# Constants!
# colors for screen information
colBgrWhite = (255, 255, 255)

# fonts for displaying text
font = cv2.FONT_HERSHEY_SIMPLEX

def displayUserInstructions(promptUser):

    # create empty bgr image for the test
    bgrUserInstructions = np.zeros(shape=[240, 320, 3], dtype=np.uint8)

    cv2.putText(bgrUserInstructions, 'Press <esc> or \'q\' to exit', (20, 40), font, 0.5, colBgrWhite, 1, cv2.LINE_AA)
    cv2.putText(bgrUserInstructions, 'Press the letter \'i\' to', (20, 60), font, 0.5, colBgrWhite, 1, cv2.LINE_AA)
    cv2.putText(bgrUserInstructions, '     move backwards in images', (20, 80), font, 0.5, colBgrWhite, 1, cv2.LINE_AA)
    cv2.putText(bgrUserInstructions, 'Press the letter \'m\' to', (20, 100), font, 0.5, colBgrWhite, 1, cv2.LINE_AA)
    cv2.putText(bgrUserInstructions, '     move forwards in images', (20, 120), font, 0.5, colBgrWhite, 1, cv2.LINE_AA)

    cv2.putText(bgrUserInstructions, 'Press any key to begin or refresh', (20, 160), font, 0.5, colBgrWhite, 1, cv2.LINE_AA)

    # display the test image to verify it visually
    cv2.imshow('These are the user instructions', bgrUserInstructions)

    # if prompt user is true then
    if promptUser:
        # wait for user input to move or close
        k = cv2.waitKey(0)
        return k
    else:
        return 0

if __name__ == "__main__":

    # create empty bgr image for the test
    k = displayUserInstructions(True)

    # 
    print('k = ', k)

    # cleanup and exit
    cv2.destroyAllWindows()