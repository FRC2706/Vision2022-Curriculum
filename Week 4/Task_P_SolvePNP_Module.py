import math
import cv2
import numpy as np

#Computer the final output values, 
#angle 1 is the Yaw to the target
#distance is the distance to the target
#angle 2 is the Yaw of the Robot to the target

def compute_output_values(rvec, tvec):
    '''Compute the necessary output distance and angles'''

    # The tilt angle only affects the distance and angle1 calcs
    # This is a major impact on calculations
    tilt_angle = math.radians(0)

    x = tvec[0][0]
    z = math.sin(tilt_angle) * tvec[1][0] + math.cos(tilt_angle) * tvec[2][0]

    # distance in the horizontal plane between camera and target
    distance = math.sqrt(x**2 + z**2)

    # horizontal angle between camera center line and target
    angleInRad = math.atan2(x, z)
    angle1 = math.degrees(angleInRad)

    rot, _ = cv2.Rodrigues(rvec)
    rot_inv = rot.transpose()
    pzero_world = np.matmul(rot_inv, -tvec)
    angle2InRad = math.atan2(pzero_world[0][0], pzero_world[2][0])
    angle2 = math.degrees(angle2InRad)

    return distance, angle1, angle2