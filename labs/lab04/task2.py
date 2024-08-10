#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import easygopigo3 as go  #import easygopigo3 to control the robot 
import time    #imports time 


def main():  # a function
    myRobot = go.EasyGoPiGo3() #to control the robot, define go.EasyGoPiGo3() to be myRobot

    myRobot.set_speed(500)  #setting the robots speed 
    myRobot.forward()  #telling the robot to go forward
    time.sleep(1)  #continue moving forward fot for a particular time
    myRobot.right()  #then robot turns right
    time.sleep(0.5)  #keep turning right for a particular time
    myRobot.backward() #robot moves back
    time.sleep(1) #keep moving back 
    myRobot.stop() #robot stop
    myRobot.orbit(90, 5) #make the robot orbit around an object at 90 degree to the right in radius of 5
    myRobot.orbit(-90, 5) ##make the robot orbit around an object at 90 degree to the leftin radius of 5
    myRobot.stop() #make the robot stop


if __name__ == "__main__": #set a condition to call the function
    main() #call the main function
