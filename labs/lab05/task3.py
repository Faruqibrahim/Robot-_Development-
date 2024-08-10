#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

# default trackbar value
trackbar_value = 127

def main():
    # Working with image files stored in the same folder as .py file
    file = "sample01.tiff"

    # Load the image from the given location
    img = cv2.imread(file)

    # Load the image from the given location in greyscale
    img_greyscale = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    while True: 
        # Thresholding the grayscaled image 
        ret, thresh = cv2.threshold(img_greyscale, trackbar_value, 255, cv2.THRESH_BINARY)
    
        # Display the images
        cv2.imshow("Original", img)
        cv2.imshow("Threshold", thresh)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()