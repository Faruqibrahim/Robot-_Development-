#!/usr/bin/env python3
# -- coding: utf-8 --

import cv2
import numpy as np
import time
import easygopigo3 as go


file_name = "default_trackbar.txt"

lH =0
lS = 0
lV = 0
hH = 0
hS = 0
hV = 0
exposure = 200
white_balance = 3000

# NB! This function will be re-used in the future labs
def get_values_from_file(file_name):
    global lH,lS,lV,hH,hS,hV
    f = open(file_name, "r")
    #print(f.read())    
    values = f.read().split()    
    for t in range(len(values)):
        values[t]=int(values[t])
    exposure = values[0]
    white_balance = values[1]    
    lH =values[2]
    lS = values[3]
    lV = values[4]
    hH = values[5]
    hS = values[6]
    hV = values[7]

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

#create new value for trackbar
camera = cv2.VideoCapture(0)

def cam_reset():
    global camera
#     camera.release()
#     camera = cv2.VideoCapture(0)
    camera.read()

def main():
    global camera
    my_Robot = go.EasyGoPiGo3()
    # Open the camera
    
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
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        my_Robot.set_speed(200)      
        #this code below is to ensure that when we have two blops,
        #we get the mid point betweem the poles and cneter this mid point
        #with the center of the frame.
        if len(keypoints) == 2:
            print(1)
            mid_point = (keypoints[0].pt[0]+keypoints[1].pt[0])/2

            if mid_point>325:
                my_Robot.steer(20, -20) 
            elif mid_point<315:
                my_Robot.steer(-20, 20) 
            else:
                if keypoints[0].pt[0] < keypoints[1].pt[0]:
                    left = keypoints[0]
                    right = keypoints[1]
                else:
                    right = keypoints[0]
                    left = keypoints[1]
                print(left.size-right.size)
                #if the absolute difference is less than 8 pixels and if the
                #distance is greater than 400, the robot moves forward.
                if abs(left.size-right.size) < 8:
                    if (right.pt[0]-left.pt[0] > 400):
                        my_Robot.forward()
                        time.sleep(10)
                        break
                    my_Robot.forward()
                    time.sleep(1)
                    #we need to always reset camera when we make robot sleep
                    #to prevent buffering.
                    #cam_reset()
                elif left.size > right.size:
                    my_Robot.turn_degrees(60)
                    my_Robot.forward()
                    time.sleep(1)
                    my_Robot.turn_degrees(-60)
                    #same here as above 
                    #cam_reset()
                    
                else:
                   my_Robot.turn_degrees(-60)
                   my_Robot.forward()
                   time.sleep(1)
                   my_Robot.turn_degrees(60)
                   #cam_reset()                 
      #thhe code below allows the robot to keep rotating if it finds less than two blops
        if (len(keypoints) < 2):
            my_Robot.steer(20, -20)
         #display original image 
        cv2.imshow("Original", img_new)
        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()
    my_Robot.stop()
    
#     f = open(file_name, "w")
#     f.write(str(exposure)+" "+str(white_balance)+" "+str(lH)+" "+str(lS)+" "+str(lV)+" "+str(hH)+" "+str(hS)+" "+str(hV))
#     f.close()

if __name__ == "__main__":
    main()