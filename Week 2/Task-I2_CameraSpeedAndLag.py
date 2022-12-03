# This is a pseudo code file for Merge Robotics

# This is task I2 - > Camera Speed and Lag.  Let's follow the steps that our work in Visions takes
# on the robot.  1) Camera takes picture.  2) Raspberry Pi offers that image up to Python. 3) our code
# analyses the image and does some math.  3) the FIRST provided image and it's server puts the original
# image and anything we create into a video stream that gets sent over ethernet to the radio on the 
# robot.  4) the radio using wifi sends the stream onto the field network destined for our driver station
# laptop.  5) the laptop running the FIRST provided software reads the stream and displays it for the
# drive team.  6) The drive team takes action.

# It turns out that the above takes time, small bits of it, but enough that there is a lag between an event
# happening in the real world and the driver station presenting that to the drive team.  Sometimes way 
# too much time.

# Do some research and see what you can find out about this problem and maybe waht other team are doing about
# it.  Add your found links to ".py" version of this file and do a pull request.

# https://raspberrypi.stackexchange.com/questions/58871/pi-camera-v2-fast-full-sensor-capture-mode-with-downsampling

# https://www.reddit.com/r/computervision/comments/4732ir/camera_for_realtime_image_processing/

# https://makehardware.com/2016/03/29/finding-a-low-latency-webcam/

# concept called binning that gets turned on or off on the camera to speed it up

# Here are some links related to compensating for lag in a vision system
# https://www.chiefdelphi.com/t/help-with-logging-gyro-data-for-vision-lag-compensation/161480
# https://pdocs.kauailabs.com/sf2/examples/video-processing-latency-correction/

