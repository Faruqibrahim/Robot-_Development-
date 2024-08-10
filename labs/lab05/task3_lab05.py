#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# default trackbar value
trackbar_value = 127

# Open the default video camera
camera = cv2.VideoCapture(0)

# Global variable for the latest trackbar value (exposure is a float here)
threshold_value = camera.get(cv2.CAP_PROP_EXPOSURE)

# A callback function for a trackbar
# It is triggered every time the trackbar slider is used
##create new value for the trackbar
def update_threshold_value(new):
    global trackbar_value
    trackbar_value = new
    #camera.set(cv2.CAP_PROP_EXPOSURE, new)

def main():
    # Working with image files stored in the same folder as .py file
    file = "sample02.tiff"

    # Load the image from the given location
    img = cv2.imread(file)

    # Load the image from the given location in greyscale
    img_greyscale = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    
    # Create a named window and name it "Output"
    cv2.namedWindow("Output")
    
    #create trackbar
    cv2.createTrackbar("Threshold_value", "Output", int(threshold_value), 255, update_threshold_value)
    
    
    blobparams = cv2.SimpleBlobDetector_Params()
    
    # filtering blobs by area
    blobparams.filterByArea = True
    blobparams.minArea = 500
    blobparams.maxArea = 100000

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
    
    cv2.rectangle(img_greyscale, (0, 0), (1280, 720), (255, 0, 0), 5)

    while True: 
        # Thresholding the grayscaled image 
        ret, thresh = cv2.threshold(img_greyscale, trackbar_value, 255, cv2.THRESH_BINARY)
    
        # Display the images
        cv2.imshow("Threshold", thresh)
        cv2.imshow("greyscale", img_greyscale)
        
        #call the detector and save as keypoints
        keypoints = detector.detect(thresh)
        
        #show the detected keypoints in the window
        img_new = cv2.drawKeypoints(img, keypoints, None, (0, 225, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        #print (img_new.shape)
        
        
        #this is for the keypoint coordinates 
        for i in range(len(keypoints)):
            x = keypoints[i].pt[0]
            y = keypoints[i].pt[1]
            
            #write the coordinate x and y in the dtected blops
            cv2.putText(img_new, str(x) + " " +str(y),(int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 125, 255), 2)
            
            cv2.imshow("Original", img_new)
        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
