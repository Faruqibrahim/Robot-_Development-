#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import easygopigo3 as go
import numpy as np
import time


file_name = "default_trackbar.txt"

lH =0
lS = 0
lV = 0
hH = 0
hS = 0
hV = 0

# NB! This function will be re-used in the future labs
def get_values_from_file(file_name):
    global lH,lS,lV,hH,hS,hV
    f = open(file_name, "r")
    
    #print(f.read())
    
    values = f.read().split()
    
    for t in range(len(values)):
        values[t]=int(values[t])
        
    lH =values[0]
    lS = values[1]
    lV = values[2]
    hH = values[3]
    hS = values[4]
    hV = values[5]


# Global variable for determining GoPiGo speed
gospeed = 200

# Global variable for video feed
camera = None

# Global variable for robot object
my_robot = go.EasyGoPiGo3()


def init():
    global camera
    # This function should do everything required to initialize the robot
    # Some of this has already been filled in
    # You are welcome to add your own code if needed

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    camera.read()
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)

    my_robot.set_speed(gospeed) # This sets the maximum speed of the GoPiGo
    
    #create window name as output 
    cv2.namedWindow("Output")
    
    get_values_from_file(file_name)


# TASK 1
def get_line_location(frame):
    # This function should use a single frame from the camera to determine line location
    # It should return the location of the line in the frame
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hH, hS, hV])
    #we reduce the frame size of the image 
    frame = frame[215:265]
    # convert BGR to HSV
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    #to interchange the "0" and "1"
    img_r = cv2.bitwise_not(thresholded)
    #the code below allows to to tuple out the vertical and horizontal
    #cordinates of the nonzero pixels of a black and white image(thresholded)
    non_zero = np.nonzero(img_r)
    #the code below gets the mean of the horizontal cordinate, which is
    #second in the list hence [1]
    print(np.mean(non_zero[1]))
    
    cv2.imshow('Original', frame)       
    cv2.imshow("ThVesholded", thresholded)
    #print(str(lH) + " " + str(lS) + " " + str(lV))
    #we need to return the value of the mean to the function
    return np.mean(non_zero[1])
    # Our operations on the frame come here

    #pass


# TASK 2
def bang_bang(linelocation):
    # This function should use the line location to implement a simple bang-bang controller
    # YOUR CODE HERE

    pass


# TASK 3
def bang_bang_hysteresis(linelocation):
    # This function should use the line location to implement a bang-bang controller with hysteresis
    # YOUR CODE HERE

    pass


# TASK 4
def proportional_controller(linelocation):
    # This function should use the line location to implement a proportional controller
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE

    pass


# TASK 5
def pid_controller(linelocation):
    # This function should use the line location to implement a PID controller
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE

    pass

def main():
    try:
        while True:
            # We read information from the camera
            ret, frame = camera.read()
            cv2.imshow('Original', frame)

            # Task 1: uncomment the following line and implement get_line_location function
            linelocation = get_line_location(frame)

            # Task 2: uncomment the following line and implement bang_bang function
            # bang_bang(linelocation)

            # Task 3: uncomment the following line and implement bang_bang_hysteresis function
            # bang_bang_hysteresis(linelocation)

            # Task 4: uncomment the following line and implement proportional_controller function
            # proportional_controller(linelocation)

            # Task 5: uncomment the following line and implement pid_controller function
            # pid_controller(linelocation)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Got KeyBoardInterrupt, closing program.")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        my_robot.stop()

if __name__ == "__main__":
    # Initialisation
    init()
    # Calling the main function
    main()

