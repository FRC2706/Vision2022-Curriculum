import numpy as np

def load_camera_details(cameraId):

    cameraFound = False

    # this is the SketchUp Camera cropped and resized to 320x240...
    if cameraId == 52:
        cameraFound = True

        # from camera calibrations files 
        camera_matrix = np.array([
            [272.36049320004605, 0.0, 157.62816826544375], 
            [0.0, 257.46612122321454, 98.90302088583047],
            [0.0, 0.0, 1.0]
            ], dtype = 'double')

        dist_coeffs = np.array([
            [1.5298022258256136, -17.6800174425778, 0.05117671205418792, -0.04020311562261712, 44.20234463669946]
            ], dtype = 'double')

    if cameraFound:
        return camera_matrix, dist_coeffs
    else:
        return None, None
