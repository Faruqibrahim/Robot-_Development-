import cv2
import math

from helper.FieldDisplay import *
from helper.Node import *
from task2_aruco import *


def createField(markers):
    # <-- Write a function for creating a 2d field of numbers like in task1, where
    # the ArUco markers show the obstacles.
    return field

def main():
    # read the image from file
    frame = cv2.imread('example.jpg', 0)

    markers = detect(frame)

    # Display the resulting image with markers
    cv2.imshow('markers', frame)

    # Create the field from the image
    field = createField(markers)

    # Create the pathfinding nodes for visualization
    nodes, start, finish = createNodesFromField(field)

    display = FieldDisplay(len(frame[0]), len(frame), len(nodes[0]), len(nodes))
    display.draw_map(nodes)

    # Quit the program when any key is pressed
    cv2.waitKey(0)

    # When everything done, release the capture
    print('closing program')
    cv2.destroyAllWindows()
    display.close()

if __name__ == "__main__":
	main()