#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time

# Colour detection limits
lB = 0
lG = 0
lR = 95
hB = 100
hG = 100
hR = 184

#update the trackbar values

def update_lB(new):
    global lB
    lb =new
    
def update_hB(new):
    global hB
    hb =new
    
def update_lG(new):
    global lG
    lG =new
    
def update_hG(new):
    global hG
    hG =new
    
def update_lR(new):
    global lR
    lR =new
    
def update_hR(new):
    global hR
    hR =new

def main():
    # Open the camera
    camera = cv2.VideoCapture(0)
    
    cv2.namedWindow("Output")

    cv2.createTrackbar("lB", "Output", lB, 255, update_lB)
    cv2.createTrackbar("hB", "Output", hB, 255, update_hB)
    cv2.createTrackbar("lG", "Output", lG, 255, update_lG)
    cv2.createTrackbar("hG", "Output", hG, 255, update_hG)
    cv2.createTrackbar("lR", "Output", lR, 255, update_lR)
    cv2.createTrackbar("hR", "Output", hR, 255, update_hR)
    
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
        lowerLimits = np.array([lB, lG, lR])
        upperLimits = np.array([hB, hG, hR])

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



        cv2.imshow("Original", img_new)

        # Display the resulting frame
        cv2.imshow("Thresholded", thresholded)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

