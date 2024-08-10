# -*- coding: utf-8 -*-

from ..helper.current_state import CurrentState

# Feel free to add variables and helper functions to this file.
# Do NOT rename or remove the given functions!

raspberry_pico = CurrentState().get_raspberry_pico()  # Use this object to access sensor values from the raspberry pico, see example in drive loop
robot = CurrentState().get_gopigo()  # This is the same gopigo robot object that you have used in previous labs

# Fill this list with marker distances and use it to check them. The furthest marker has index 0.
marker_distances = [1800, 1600, 1300, 900, 600, 400, 200]


def follow_line(should_close):
    # Do NOT rename or remove this function!
    robot.reset_encoders()
    robot.set_speed(100)  # feel free to change this

    while not should_close.isSet():
        line_sensor_values = raspberry_pico.get_line_sensor_dict()  # This returns you the current values of line sensors as python dict
        current_marker_index = CurrentState().get_current_marker_index()  # Use this to get the current marker index
#         print(line_sensor_values)  # So you can see the whole dict to find the keys
#         print(line_sensor_values["IR_LEFT"])  # This is how to access one line sensor value
#         print(current_marker_index)  # Prints -1 since no marker detection has been implemented

        # Add your line following logic here
        #since its indexing it counts from 0 and stops at 6
        if current_marker_index == 6:
            robot.steer(0, 0)
        else:

            robot.forward()
            #this condition is to say that if the light sensor in the middle
            #senses black line, it should go right and left if otherwise 
            if line_sensor_values["IR_MID"] == 0:
                robot.right()
            else:
                robot.left()

        should_close.wait(0.02)

def check_markers(marker_sensor_value, current_marker_index):
    global was_marker
    """
    Do NOT rename or remove this function!
    Use the line sensor connected to the Raspberry Pi Pico to detect markers next to the line. 
    If a new marker is detected then print the distance from it to the wall.
    :param marker_sensor_value: line sensor value that you use for marker detection
    :param current_marker_index: index of current marker
    :return: current_marker_index if no new marker detected or index of new marker
    """
    #this condition is to check if the value is 0 i.e there is black line and
    #no marker is detected, it should count by adding 1
    if marker_sensor_value == 0 and not was_marker:
        current_marker_index += 1
        print(current_marker_index, marker_distances[current_marker_index])
        was_marker = True
            
    elif marker_sensor_value == 1:
        #this is to update the state of the marker detection
        was_marker = False
    

    return current_marker_index
