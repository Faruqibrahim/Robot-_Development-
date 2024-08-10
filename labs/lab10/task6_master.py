import cv2

from helper.Drive import *
from task1_astar import *
from task2_aruco import *
from task3_field import *
from task4_path import *
from task5_command import *

def main():
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	# read one frame before changing camera settings to ensure they all take effect
	ret, frame = cap.read()
	cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
	cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
	cap.set(cv2.CAP_PROP_AUTO_WB, 1)
	
	# Change these values if the markers are difficult to detect
	cap.set(cv2.CAP_PROP_FOCUS, 35)
	cap.set(cv2.CAP_PROP_EXPOSURE, 400)


	# <-- You can set other camera parameters to improve markers detection  


	ret, frame = cap.read()

	# <-- Change the robot id number to the one written on the tag you're using
	robotID = 1

	# <-- Find the markers from the frame and calculate the shortest path


	# drive = Drive(path)
	commander = Commander(IP_ADDRESS, PORT_NR)
	
	try:
		while True:
			# if drive.arrived: break

			# read the image from the camera
			ret, frame = cap.read()

			markers = detect(frame)

			# Display the resulting image with markers
			cv2.imshow('markers', frame)

			# <-- Find the coordinates of the front and back of the robot, get the next command from the drive object and pass it on to the commander

			# Quit the program when Q is pressed
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	finally:
		commander.sendCommand('S')  # Just in case
		commander.closeSocket()
		cap.release()
		cv2.destroyAllWindows()

if __name__ == "__main__":
	main()