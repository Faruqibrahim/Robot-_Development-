#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import os.path



file_name = "lab05/default_trackbar.txt"

#path = './default.txt'


file_name = "lab05/default_trackbar.txt"

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

### TODO 1: Add code from task 5
### TODO 2: Once the main loop is exited, new trackbar values should be written into a text file (that is going to be in a specific lab folder)
### TODO 3: Fill in the get_values_from_file() function which reads in the text file and outputs trackbar values
### TODO 4: Run this program at least twice to make sure the trackbar values are written and read from the text file
    
#open the camera
camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv2.CAP_PROP_AUTO_WB, 0)

exposure = camera.get(cv2.CAP_PROP_EXPOSURE)

white_balance = camera.get(cv2.CAP_PROP_EXPOSURE)

def update_exposure(new):
    global exposure
    exposure = new
    camera.set(cv2.CAP_PROP_EXPOSURE, new)
    
def update_white_balance(new_l):
    global white_balance
    white_balance = new_l
    camera.set(cv2.CAP_PROP_WB_TEMPERATURE, new_l)

#update the trackbar values

def update_lH(new):
    global lH
    lH =new
    
def update_hH(new):
    global hH
    hH =new
    
def update_lS(new):
    global lS
    lS =new
    
def update_hS(new):
    global hS
    hS =new
    
def update_lV(new):
    global lV
    lV =new
    
def update_hV(new):
    global hV
    hV =new



def main():
    # This function should run successfully even when there is no text file in the folder
    # get_values_from_file(###add text file path here###)
    
    
    get_values_from_file(file_name)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    
    cv2.namedWindow("Output")
    
    cv2.createTrackbar("Exposure", "Output", int(exposure), 2047, update_exposure)
    cv2.createTrackbar("White balance", "Output", int(white_balance), 6500, update_white_balance)
    
    
    
    cv2.createTrackbar("lH", "Output", lH, 255, update_lH)
    cv2.createTrackbar("hH", "Output", hH, 255, update_hH)
    cv2.createTrackbar("lS", "Output", lS, 255, update_lS)
    cv2.createTrackbar("hS", "Output", hS, 255, update_hS)
    cv2.createTrackbar("lV", "Output", lV, 255, update_lV)
    cv2.createTrackbar("hV", "Output", hV, 255, update_hV)
    
    blobparams = cv2.SimpleBlobDetector_Params()
    
    # filtering blobs by area
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
    blobparams.minDistBetweenBlobs = 10
    
    #create blop detector here
    detector = cv2.SimpleBlobDetector_create(blobparams)
    
    frame_new = 0
    frame_prev = 0
    
    while True:
        # Read the image from the camera
        ret, frame = camera.read()

        # You will need this later
        # frame = cv2.cvtColor(frame, ENTER_CORRECT_CONSTANT_HERE)

        # Colour detection limits
        lowerLimits = np.array([lH, lS, lV])
        upperLimits = np.array([hH, hS, hV])

        # Our operations on the frame come here
        thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
        
        img_r = cv2.bitwise_not(thresholded)
        
        keypoints = detector.detect(img_r)
        
        img_new = cv2.drawKeypoints(frame, keypoints, None, (0, 225, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

  
        #calculate frame rate
        frame_new = time.time()
        fps = 1/(frame_new-frame_prev)
        
        #update the value of new rame rate
        frame_prev = frame_new
        
        fps = str(int(fps))
        
        cv2.putText(img_new, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 125, 255), 2)
        
        for i in range(len(keypoints)):
            x = keypoints[i].pt[0]
            y = keypoints[i].pt[1]
            
            #write the coordinate x and y in the dtected blops
            cv2.putText(img_new, str(x) + " " +str(y),(int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 125, 255), 2)



        cv2.imshow("Output", img_new)
        # Display the resulting frame
        cv2.imshow("Thresholded", thresholded)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()
    
    f = open(file_name, "w")
    f.write(str(lH)+" "+str(lS)+" "+str(lV)+" "+str(hH)+" "+str(hS)+" "+str(hV))
    f.close()



if __name__ == "__main__":
    main()


