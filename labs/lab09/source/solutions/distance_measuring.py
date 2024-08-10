# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os.path

# Feel free to add variables and helper functions to this file. 
# Do NOT rename or remove the given functions!
file_name = "/home/pi/robotics-i-loti.05.010-faruq-ibrahim-c18421-23-24a/labs/lab09/source/solutions/default_trackbar.txt"

lH =0
lS = 0
lV = 0
hH = 0
hS = 0
hV = 0
exposure = 200
white_balance = 3000

def measure_with_ultrasonic(raspberry_pico):
    """
    Do NOT rename or remove this function!
    Use the pico to measure distance with ultrasonic sensor.
    :param raspberry_pico: look at pico_facade.py file to find the right function to use
    :return: measured distance from the wall
    """

    # ADD YOUR IMPLEMENTATION HERE
    
    #since we already have the ultrasonic sensor measured in raspberry_pico, we can retrieve
    #it from there, by writing this code below.
    value_ultrasonic = raspberry_pico.get_us_distance()

    return value_ultrasonic


def measure_with_encoders(robot):
    """
    Do NOT rename or remove this function!
    Use gopigo robot to measure distance with encoders.
    :param robot: same gopigo robot object that you have used in previous labs
    :return: measured distance from the wall
    """

    # ADD YOUR IMPLEMENTATION HERE
    
    #from API we measure the encoder and then subracted 1800 from it because the encoder  starts reading
    #from 0 and increases meanwhile the distance decreases from 1800 downwards as the robot moves
    #forward. Aslo, i sultiplied by 10 so as to convert its value in cm to mm
    value_encoder = 1800-robot.read_encoders_average()*10
    #here as well i have kto return the value of the encoder.
    return value_encoder

def get_values_from_file(file_name):
    check_file = os.path.isfile(file_name)
    print(check_file)
    if  check_file == True:
        
        global lH, lS, lV, hH,hS,hV, exposure, white_balance
        f = open(file_name, "r")
    
        values = f.read().split()
        print (values)
    
        for i in range(len(values)):
            values[i] = int(values[i])
        exposure = values[0]
        white_balance = values[1]
        lH = values[2]
        lS = values[3]
        lV = values[4]
        hH = values[5]
        hS = values[6]
        hV = values[7]
        
#open the camera
#camera = cv2.VideoCapture(0)

        
get_values_from_file(file_name)


blobparams = cv2.SimpleBlobDetector_Params()

#filter blop by area
blobparams.filterByArea = True
blobparams.minArea = 500
blobparams.maxArea = 1E12
# in case the blob is not perfectly circular
blobparams.filterByCircularity = False
# and could be a bit wonky
blobparams.filterByInertia = False
# and might have holes inside
blobparams.filterByConvexity = False
# don't want to detect every single small speck in the proximity
blobparams.minDistBetweenBlobs = 20

#create blop dtector
detector = cv2.SimpleBlobDetector_create(blobparams)
    

def measure_with_camera(camera):
    """
    Do NOT rename or remove this function!
    Use camera to measure distance with blob size detection.
    :param camera: the same camera object you have used in previous labs
    :return: measured distance from the wall. If no blobs are detected return None.
    """
    camera.read()
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    camera.set(cv2.CAP_PROP_AUTO_WB, 0)

    
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure)
    camera.set(cv2.CAP_PROP_WB_TEMPERATURE, white_balance)
    
    # ADD YOUR IMPLEMENTATION HERE
    ret, frame = camera.read()
    #instead of making the parameter qual to blur, i made it qual to frame,
    #if not the orgibal image will not react to the blur text bar as the
    #thVesholded have frame not blur.
    #frame = cv2.GaussianBlur(frame,(blur_kernel,blur_kernel),0)
    
    #frame = cv2.medianBlur(frame,blur_kernel)

    # convert BGR to HSV
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Colour detection limits
    lowerLimits = np.array([lH, lS, lV])
    upperLimits = np.array([hH, hS, hV])

    # Our operations on the frame come here
    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    thresholded = cv2.bitwise_not(thresholded)
    keypoints = detector.detect(thresholded)
    diamter = []
    for i in keypoints:
        diameter = i.size
        #this is to find the largest blop and hence, an empty list is first
        #creaed up
        diamter.append(diameter)
        #print(diameter)
    #here, the condition if allows thw robot to print if it doesnt see blops
    print(diamter)
    if  diamter != []:
        #using maximum distance so that when the robot is moving it doesnt return
        #values from surrrounding blops
        print("blop diameter",max(diamter))
        #we return the vslue of y which is equal to y=a/x-b where a and b are
        #the optimised parameters
        return 131941.8/max(diamter)-123.6
    
#     cv2.imshow("Output", frame)
#             # Quit the program when "q" is pressed
#     if (cv2.waitKey(1) & 0xFF) == ord("q"):
#             
# 
#     # When everything done, release the camera
#         print("closing program")
#         camera.release()
#         cv2.destroyAllWindows()
