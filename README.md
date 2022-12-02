# Vision2022-Curriculum
The vision curriculum

This repository is for Merge Robotics, 2022-2023 Season

We will be working through the tasks located in each week's folder, to:

- Learn Python
- Learn how to use Github
- Learn to use VSCode to develop code for our computers and for raspberry pi
- Learn the basic of vision processing using the powerful OpenCV open source library to solve a typical FRC vision challenge
- New to 2022!!  We will be using OpenCV tools to find April tags which will be used in the game this year

The basic workflow for FRC vision is Good Image, Good Mask and good Math. Let's call this "GIGMM"! An acronym to remember the workflow.

We will not need a robot, or specific hardware, other than a computer with Python, OpenCV and VSCode.




# How to Setup Vision development environment:

Install Visual Code studio 
   Install Viscual Code Studio extensions
   - Use Python (Intellisense from microsoft)
   - WPI extension
   - OpenCV - intellisense

   Optional:
   - Java (for robot code)
   - C/C++ for microsoft

Install python (python.org)
- install with path setting enabled
- make sure pip is installed, and other default options

Open command line (cmd in windows) - This will also verify install
- py -m pip install --upgrade pip

To install number python (more math operations)
- pip install numpy

To install open CV
- pip instal opencv-python

To get networktables (To talk to our robot)
- pip install robotpy

To install april tags
- pip3 install apriltag

Clone Vision repository
- git clone https://github.com/FRC2706/Vision2023-Competition.git

Open folder to Vision repository in VS Code
- MergeViewer lets you run the vision code from your labtop
- MergeFRCPipeline.py is the mainline use for the python code

Merge Robotics, November 2022
