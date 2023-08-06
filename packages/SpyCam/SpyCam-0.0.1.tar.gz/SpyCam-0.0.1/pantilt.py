# Inspired by Adrian Rosebrock of PyImageSearch.com
# Luca Barbas and Keagan Chasenski
# 1 October 2020
# Design Project

# import packages
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
import pantilthat as pth
import argparse
import signal
import time
import sys
import cv2



# function to handle system interrupts for signals
def interrupt_handler(sig, frame):
    """ This is a function to handle system interrupts for signals """
	# prints system message
	print("[MESSAGE] You cancelled the system process! Now Exiting...")

	# disable the servos
	# DOC: servo_enable has two arguments: servo number, state (True/False) 
	pth.servo_enable(1, False)
	pth.servo_enable(2, False)

	# exit program
	sys.exit()



# function which specifies the range
def set_range(val, start, end):
    """ States the range of movement """
	# determine the input vale is in the supplied range
	return (val >= start and val <= end)


# function centers the box in the middle of the screen
def center_object(args, objX, objY, centerX, centerY):
    """ Centers the box in the middle of the screen"""

	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, interrupt_handler)

	# video stream started to display the face detection working on
	# the monitor
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# initializes the Object Center function using the Haar-Cascade
	# Detection software
	obj = ObjCenter(args["cascade"])

	# loop indefinitely
	while True:
		# Take each frame processed from the video stream and flip the
        # camera's video stream vertically because our stream was upside
        # down
		frame = vs.read()
		frame = cv2.flip(frame, 0)

		# using the height and width, get the center coordinates of the video
		# feed to determine where the object center should be 
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		# find the face detection location
		objectLoc = obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect) = objectLoc

		# use openCV to draw the bounding box rectangle around the detected
		# location of the face
		# DOC: cv2.rectangle (frame input, center coordinates, outer coordinates,
		# RGB colour, line thickness)
		if rect is not None:
			(x, y, w, h) = rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)	

		# use OpenCV to show heading, frame 
		cv2.imshow("Pan-Tilt Face Tracking", frame)
		cv2.waitKey(1)



# function which controls the movement of the camera by moving the servos
# mechanical mechanism of the system
def synch_servos(pan, tlt):
    """ Initializes the servo motors before computation begins """

	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, interrupt_handler)

	# loop indefinitely
	while True:
            
		# reverse the Pan angle because the camera is inversed horizontally
		panAngle = -1 * pan.value
		# reverse the Tilt angle because the camera is inversed vertically
		tltAngle = -1 * tlt.value

		# check if pan angle is within range
		if set_range(panAngle, servoRange[0], servoRange[1]):
			pth.pan(panAngle)	# pan

		# check if tilt angle is within range 
		if set_range(tltAngle, servoRange[0], servoRange[1]):
			pth.tilt(tltAngle)	# tilt



# function to handle the Control Mechanism of the Pan and Tilt servo Arm 
# this uses a PID compensator 
def pid_control(output, p, i, d, objCoord, centerCoord):
	""" Returns the PID error based on the current PID values, 
		Object Coords and Center Coords
	
	Keyword arguments: 
	output -- output variable
	p -- proportional controller variable
	i -- integral controller variable
	d -- differential controller variable
	objCoord - Objects X and Y coordinates
	centerCoord - X and Y coordinate of the center of the frame
	
    """
    
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, interrupt_handler)

	# initialize the PID Controller
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# loop indefinitely
	while True:
		# find the error function
		error = centerCoord.value - objCoord.value

		# update the output value based on the error
		# DOC: The output.value variable will keep updating with a change 
		# in error value as long as the servo is moving, otherwise the 
		# error will be zero
		output.value = p.update(error)
