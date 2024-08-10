#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time

def main():
    # Open the camera
    camera = cv2.VideoCapture(0)
    
    #set frame rates to initail values of 0
    frame_new = 0
    
    frame_prev = 0
    
    while True:
        # Read the image from the camera
        ret, frame = camera.read()
        
        #calculate frame rate
        frame_new = time.time()
        fps = 1/(frame_new-frame_prev)
        
        #update the value of new rame rate
        frame_prev = frame_new
        
        fps = str(int(fps))

        # Write some text onto the frame
        cv2.putText(frame, fps, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show this image on a window named "Original"
        cv2.imshow("Original", frame)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    # When everything is done, release the camera
    print("closing program")
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
