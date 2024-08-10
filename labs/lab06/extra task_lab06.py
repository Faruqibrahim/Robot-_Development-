#!/usr/bin/env python3
# -- coding: utf-8 --

import cv2
import numpy as np
import time
import easygopigo3 as go


file_name_1 = "default_trackbar.txt"
file_name_2 = "default_trackbar2.txt"

lH =0
lS = 0
lV = 0
hH = 0
hS = 0
hV = 0

lH_2 =0
lS_2 = 0
lV_2 = 0
hH_2 = 0
hS_2 = 0
hV_2 = 0

# NB! This function will be re-used in the future labs
def get_values_from_file_1(file_name_1):
    global lH,lS,lV,hH,hS,hV
    f = open(file_name_1, "r")
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
    
def get_values_from_file_2(file_name_2):
    global lH,lS,lV,hH,hS,hV
    f = open(file_name_2, "r")
    #print(f.read())    
    values = f.read().split()    
    for t in range(len(values)):
        values[t]=int(values[t])
        
    lH_2 =values[0]
    lS_2 = values[1]
    lV_2 = values[2]
    hH_2 = values[3]
    hS_2 = values[4]
    hV_2 = values[5]

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
    camera.release()
    camera = cv2.VideoCapture(0)
    
def main():
    global camera
    my_Robot = go.EasyGoPiGo3()
    # Open the camera
    
    #create window name as output 
    cv2.namedWindow("Output")
    get_values_from_file_1(file_name_1)
    get_values_from_file_2(file_name_2)
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
    detector_2 = cv2.SimpleBlobDetector_create(blobparams)
    #used to record time when we processed current frame 
    new_frame_time = 0
    new_frame_time_2 = 0
    #use dto record time when we processed current frame 
    prev_frame_time = 0
    prev_frame_time_2 = 0
    
    double_poles = True
    while True:
        # Read the image from the camera
        if double_poles == True:
            ret, frame = camera.read()
        else:
            frame = frame[215:265]
        #instead of making the parameter qual to blur, i made it qual to frame,
        #if not the orgibal image will not react to the blur text bar as the
        #thVesholded have frame not blur.
        #frame = cv2.GaussianBlur(frame,(blur_kernel,blur_kernel),0)
        if double_poles == True:
            frame = cv2.medianBlur(frame,blur_kernel)
        else:
            frame2 = cv2.medianBlur(frame,blur_kernel)
    
        # convert BGR to HSV
        if double_poles == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        else:
            frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Colour detection limits
        if double_poles == True:
            lowerLimits = np.array([lH, lS, lV])
            upperLimits = np.array([hH, hS, hV])
        
        if double_poles == True:
            lowerLimits_2 = np.array([lH_2, lS_2, lV_2])
            upperLimits2 = np.array([hH_2, hS_2, hV_2])

        # Our operations on the frame come here
        if double_poles == True:
            thVesholded = cv2.inRange(frame, lowerLimits, upperLimits)
        else:
            thVesholded_2 = cv2.inRange(frame, lowerLimits, upperLimits)
        
        if double_poles == True:
            img_r = cv2.bitwise_not(thVesholded)
        else:
            img_r_2 = cv2.bitwise_not(thVesholded_2)
        
        if double_poles == True:
            img_r=cv2.rectangle(img_r, (0, 0), (639, 49), (255, 255, 255), 2)
        else:
            img_r_2=cv2.rectangle(img_r_2, (0, 0), (639, 49), (255, 255, 255), 2)
        
        #call the detector and save as keypoint
        if double_poles == True:
            keypoints = detector.detect(img_r)
        else:
            keypoints_2 = detector.detect(img_r_2)
            
        #show the detected keypoints in the window
        if double_poles == True:
            img_new = cv2.drawKeypoints(frame, keypoints, None, (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        else:
            img_new_2 = cv2.drawKeypoints(frame, keypoints_2, None, (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        #time when we finish processing from this frame
        if double_poles == True:
            new_frame_time = time.time()
        else:
            new_frame_time_2 = time.time()
        # fps will be number of frame processed in given time frame
        # since their will be most of time error of 0.001 second
        # we will be subtracting it to get more accurate resul
        
        if double_poles == True:
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)
            fps = str(fps)
        else:
            fps_2 = 1/(new_frame_time-prev_frame_time)
            prev_frame_time_2 = new_frame_time_2
            #make fps into integer and string to be able to print out 
            fps_2 = int(fps_2)
            fps_2 = str(fps_2)
        
        
        #write some texr on the original image, this time frame rate
        if double_poles == True:    
            cv2.putText(img_new, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText_2(img_new, fps_2, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Display the resulting frame
        if double_poles == True:
            cv2.imshow("ThVesholded", thVesholded)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            my_Robot.set_speed(100) 
        else:
            cv2.imshow("ThVesholded_2", thVesholded_2)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            my_Robot.set_speed(100)
             
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
                    cam_reset()
                elif left.size > right.size:
                    my_Robot.turn_degrees(60)
                    my_Robot.forward()
                    time.sleep(1)
                    my_Robot.turn_degrees(-60)
                    #same here as above 
                    cam_reset()
                    
                else:
                   my_Robot.turn_degrees(-60)
                   my_Robot.forward()
                   time.sleep(1)
                   my_Robot.turn_degrees(60)
                   cam_reset()                 
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
#     f.write(str(lH)+"\n"+str(lS)+"\n"+str(lV)+"\n"+str(hH)+"\n"+str(hS)+"\n"+str(hV))
#     f.close()

if __name__ == "__main__":
    main()
