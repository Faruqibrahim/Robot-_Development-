#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import easygopigo3 as go
import time
import os.path

file_name = "default_trackbar.txt"

#path = './default.txt'

# Colour detection limits
lH = 0
lS = 0
lV = 0
hH = 0
hS = 0
hV = 0

# NB! This function will be re-used in the future labs
def get_values_from_file(file_name):
    #This function reads the text file and returns all of the trackbar values
    check_file = os.path.isfile(file_name)
    if  check_file == True:
        
        global lH, lS, lV, hH,hS,hV
        f = open(file_name, "r")
    
        values = f.read().split()
        print (values)
    
        for i in range(len(values)):
            values[i] = int(values[i])
        
            lH = values[0]
            lS = values[1]
            lV = values[2]
            hH = values[3]
            hS = values[4]
            hV = values[5]


#blur must be odd, hence i set to 1
#if set to 0, it will be even
blur_kernel = 1

#create a call back function for the blur 
def update_blur(new):
    global blur_kernel
    blur_kernel = new
    #here i need to make the blur always be odd.
    #if its even, it doesnt work well from the matrix
    #because after selecting the middle point of the matrix
    #we should have a sqaure matrix below and above the mid point
    #this can only be achieved having an odd order of matrix
    if blur_kernel % 2 == 0:
        blur_kernel += 1

def main():
    
    my_Robot = go.EasyGoPiGo3()
    
    # Open the camera
    camera = cv2.VideoCapture(0)
    
    #create window name as output 
    cv2.namedWindow("Output")
    
    get_values_from_file(file_name)
    
    
    #create trackbar for the blur
    cv2.createTrackbar("blur", "Output", blur_kernel, 255, update_blur)
      
     #initqialise blobdetector and name it blopparam
    blobparams = cv2.SimpleBlobDetector_Params()
    
    
    #filter blop by area
    blobparams.filterByArea = True
    blobparams.minArea = 500
    blobparams.maxArea = 1E8
    

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
    
    #used to record time when we processed current frame 
    new_frame_time = 0
    
    #use dto record time when we processed current frame 
    prev_frame_time = 0
    
    while True:
        # Read the image from the camera
        ret, frame = camera.read()
        frame = frame[215:265]
        
        #instead of making the parameter qual to blur, i made it qual to frame,
        #if not the orgibal image will not react to the blur text bar as the
        #thVesholded have frame not blur.
        #frame = cv2.GaussianBlur(frame,(blur_kernel,blur_kernel),0)
        
        frame = cv2.medianBlur(frame,blur_kernel)
    
        # convert BGR to HSV
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Colour detection limits
        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hH, hS, hV])
        print(lowerLimits)

        # Our operations on the frame come here
        thVesholded = cv2.inRange(frame, lowerLimits, upperLimits)
        
        img_r = cv2.bitwise_not(thVesholded)
        
        img_r=cv2.rectangle(img_r, (0, 0), (639, 49), (255, 255, 255), 2)
        
        
        
        #call the detector and save as keypoint 
        keypoints = detector.detect(img_r)
        
        
        
        #show the detected keypoints in the window
        img_new = cv2.drawKeypoints(frame, keypoints, None, (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
         #time when we finish processing from this frame
        new_frame_time = time.time()
        
        # fps will be number of frame processed in given time frame
        # since their will be most of time error of 0.001 second
        # we will be subtracting it to get more accurate resul
        fps = 1/(new_frame_time-prev_frame_time)
        
        prev_frame_time = new_frame_time
        
        #make fps into integer and string to be able to print out 
        fps = int(fps)
        fps = str(fps)

        #write some texr on the original image, this time frame rate
        cv2.putText(img_new, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
        # Display the resulting frame
        cv2.imshow("ThVesholded", thVesholded)
        for i in range(len(keypoints)):
            x = keypoints[i].pt[0] 
            y = keypoints[i].pt[1]
            
            if x>340:
                my_Robot.set_speed(50)
                my_Robot.spin_right()
            elif x<300:
                my_Robot.set_speed(50)
                my_Robot.spin_left()
            else:
                my_Robot.steer(0, 0)
       
            #write the coordinates of x and y on the detected blops 
            cv2.putText(img_new, str(int(x))+" "+str(int(y)), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
      #I added this lines of code below so that when the robot do
      #doesnt see a blop, it doesnt keep turning right or turning
      #left as in the case of when it sees a blop and rather stops.
        if (len(keypoints) == 0):
            my_Robot.steer(0, 0)
         #display original image 
        cv2.imshow("Original", img_new)
        
        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()