# -*- coding: utf-8 -*-

# Feel free to add variables and helper functions to this file.
# Do NOT rename or remove the given functions!
value_pos = []
N = 5
def moving_average(pos):
    global value_pos
    """
    Do NOT rename or remove this function!
    Implement a moving average filter.
    :param pos: The latest value that is passed to the filter
    :return: The filtered value
    """
    #add the pos(last position reading) value to the list
    value_pos.append(pos)
    #if the list is above 50, splice out ther first value
    if len(value_pos) > N:
        value_pos.pop(0)
    #take the average
    avg_value = sum(value_pos)/len(value_pos)
    
    return avg_value