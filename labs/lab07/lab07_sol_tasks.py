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
exposure = 200
white_balance = 3000

new_time = 0
prev_time = time.time()
new_e = 0
prev_e = 0
I_sum = 0

# NB! This function will be re-used in the future labs
def get_values_from_file(file_name):
    global lH,lS,lV,hH,hS,hV,exposure,white_balance
    f = open(file_name, "r")
    #print(f.read())
    
    values = f.read().split()
    print (values)
    for t in range(len(values)):
        values[t]=int(values[t])
        
    exposure = values[0]
    white_balance = values[1]
    lH = values[2]
    lS = values[3]
    lV = values[4]
    hH = values[5]
    hS = values[6]
    hV = values[7]


# Global variable for determining GoPiGo speed
gospeed = 1000 

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
    #img_r = cv2.bitwise_not(thresholded)
    #the code below allows to to tuple out the vertical and horizontal
    #cordinates of the nonzero pixels of a black and white image(thresholded)
    non_zero = np.nonzero(thresholded)
    #the code below gets the mean of the horizontal cordinate, which is
    #second in the list hence [1]
    # Our operations on the frame come here
    cv2.imshow('Original', frame)       
    cv2.imshow("ThVesholded", thresholded)
    #it should only get the mean if the list is not empty. Hence, preventing error messages
    if non_zero[1].size != 0:
        print(np.mean(non_zero[1]))
        #we need to return the value of the mean to the function
        return np.mean(non_zero[1])
    else:
        return None
    pass

# TASK 2
def bang_bang(linelocation):
    # This function should use the line location to implement a simple bang-bang controller
    # YOUR CODE HERE
    #the robot moves forward
    my_robot.forward()
    #since the mide point of the frame is 640, it should turn right
    #if the linelocation is greater than 640 and do otherwise if less.
    if linelocation == None:
        my_robot.stop()
    elif linelocation > 640:
        my_robot.right()
    elif linelocation < 640:
        my_robot.left()
    pass


# TASK 3
state = "Right"
def bang_bang_hysteresis(linelocation):
    global state
    # This function should use the line location to implement a bang-bang controller with hysteresis
    # YOUR CODE HERE
#     if linelocation == None:
#         my_robot.stop()
    if linelocation == None:
        my_robot.stop()
    elif state == "Right":
        my_robot.steer(80, 100)
        if linelocation > 810:
            state = "Left"
            
    elif state == "Left":
        my_robot.steer(100, 80)
        if linelocation < 570:
            state = "Right"
    pass
# TASK 4
def proportional_controller(linelocation):
    # This function should use the line location to implement a proportional controller
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE
    if linelocation != None:   
        P_out = (640-linelocation)*0.8
        my_robot.set_motor_dps(my_robot.MOTOR_LEFT,500-P_out)
        my_robot.set_motor_dps(my_robot.MOTOR_RIGHT,500+P_out)
    else:
        my_robot.stop()

# TASK 5
def pid_controller(linelocation):
    global I_sum
    global prev_e
    global prev_time
    # This function should use the line location to implement a PID controller
    # Feel free to define and use any global variables you may need
    # YOUR CODE HERE
    if linelocation != None:
        k_U = 0.9
        T_U = 1.75
        K_D = (5*k_U*T_U)/40
        k_I = (1.2*k_U)/T_U
        k_P = 0.6*k_U
        new_e = (640-linelocation)
        new_time = time.time()
        change_in_time = new_time-prev_time
        I = new_e*change_in_time
        change_in_e = new_e-prev_e

        prev_time = new_time
        prev_e = new_e

        I_sum += I
        D = change_in_e/change_in_time
        R = (k_P*new_e)+(k_I*I_sum)+(K_D*D)
        print("proportional: " + str(k_P*new_e) + "integral: " + str(k_I*I_sum) +"diff: " + str(K_D*D))
        
        my_robot.set_motor_dps(my_robot.MOTOR_LEFT,500-R )
        my_robot.set_motor_dps(my_robot.MOTOR_RIGHT,500+R)
    else:
        my_robot.steer(0, 0)

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
            #bang_bang(linelocation)

            # Task 3: uncomment the following line and implement bang_bang_hysteresis function
            #bang_bang_hysteresis(linelocation)

            # Task 4: uncomment the following line and implement proportional_controller function
            #proportional_controller(linelocation)

            # Task 5: uncomment the following line and implement pid_controller function
            pid_controller(linelocation)

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

