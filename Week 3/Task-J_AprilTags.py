# Credit to this tutorial for the apriltag code: https://pyimagesearch.com/2020/11/02/apriltag-with-python/
# Credit to this random file I found on github for the solvePnp with SOLVEPNP_IPPE_SQUARE: https://github.com/AeroTec-UAV-ART/UAV-ART/blob/b02e19ce9d569c3efb9297bd0d8fe31f54d381cd/vision/Fiduciary_Markers/Old_Code/Old_Markers_Code/markerC_new_measure.py

# Some good documentation here for a different python wrapper:
# https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample/blob/main/README_EN.md

# To install on Mac or PC
# 'pip3 install pupil-apriltags'

# To install on Linux or Raspberry pi, this should work
# 'pip3 install apriltags'
# Must uncomment the apriltag and line 47 and 48, then comment line 12 and 50-58 to work with apriltags

#import apriltag
from pupil_apriltags import Detector
import cv2
import numpy as np
from math import degrees

# Marker size and object
marker_size = 5 + 15/16.0   # FRC targets might be a different size

# Data about the marker for solvePnP's SOLVEPNP_IPPE_SQUARE stuff
object_points = []
object_points.append( [float(-marker_size / 2),float(marker_size / 2), 0])
object_points.append( [float(marker_size / 2),float(marker_size / 2), 0])
object_points.append(  [float(marker_size / 2),float(-marker_size / 2), 0])
object_points.append(  [float(-marker_size / 2),float(-marker_size / 2), 0])
object_points = np.array(object_points)
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

sucess, image = cap.read()

H_FOCAL_LENGTH, V_FOCAL_LENGTH = 640, 480
size = image.shape

camera_distortion = np.zeros((4,1))

focal_length = size[1]
center = (size[1]/2, size[0]/2)
camera_matrix = np.array(
					[[H_FOCAL_LENGTH, 0, center[0]],
					[0, V_FOCAL_LENGTH, center[1]],
					[0, 0, 1]], dtype = "double"
					)
# camera_matrix = np.array([[343.8444021316304, 0.0, 150.06626518215066], [0.0, 344.53827467342745, 105.60299945602793], [0.0, 0.0, 1.0]])
# setup apriltag detector
#options = apriltag.DetectorOptions(families="tag36h11")
#detector = apriltag.Detector(options)

detector = Detector(
   families="tag16h5",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.5,
)

while(True): 
    sucess, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	# Find all the apriltags
    results = detector.detect(gray)
    
    # loop over the AprilTag detection results
    for r in results:
        
        if (r.hamming == 0):
           (ptA, ptB, ptC, ptD) = r.corners
        
           # extract the bounding box (x, y)-coordinates for the AprilTag
		   # and convert each of the (x, y)-coordinate pairs to integers
           ptB = (int(ptB[0]), int(ptB[1]))
           ptC = (int(ptC[0]), int(ptC[1]))
           ptD = (int(ptD[0]), int(ptD[1]))
           ptA = (int(ptA[0]), int(ptA[1]))

		# draw the bounding box of the AprilTag detection
           cv2.line(image, ptA, ptB, (0, 255, 0), 2)
           cv2.line(image, ptB, ptC, (0, 255, 0), 2)
           cv2.line(image, ptC, ptD, (0, 255, 0), 2)
           cv2.line(image, ptD, ptA, (0, 255, 0), 2)
        
        # draw the center (x, y)-coordinates of the AprilTag
           (cX, cY) = (int(r.center[0]), int(r.center[1]))
           cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        
        # ERIK: Tag family should contain a string, "36h11" which is the family of the apriltag. 
		# FIRST says we should only have 36h11 tags so might be a good check to see if the target is good.
     
           tagFamily = r.tag_family.decode("utf-8")
		
		# Put the text for the id of the tag
           cv2.putText(image, f"id: {r.tag_id}", (ptA[0], ptA[1] - 15),
		   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		
		# Get the corners of the target in a numpy array for solvePnP
           corners = np.array(r.corners)

           pnpsucsess, rvec, tvec = cv2.solvePnP(object_points, corners, camera_matrix, camera_distortion, flags = cv2.SOLVEPNP_IPPE_SQUARE)
		
           print(	f"tag id: {r.tag_id} \n"
			 	f"translation vector -> x:{float(tvec[0]):.3f}, y:{float(tvec[1]):.3f}, z:{float(tvec[2]):.3f} \n"
			  	f"rotation vector    -> 1:{degrees(float(rvec[0])):.3f}, 2:{degrees(float(rvec[1])):.3f}, 3:{degrees(float(rvec[2])):.3f} \n"
			#   f"{r}"
			 	 "\n")

    cv2.imshow("Image", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break