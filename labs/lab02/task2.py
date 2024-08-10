#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin
import utime
import time


def show_row(row_number, columns, delay):
    # Control a row of the dot matrix display
    # YOUR CODE GOES HERE:
    pass     # Remove this line when implementing
    
    #to turn light on. row is high and column is low
    row_pins[row_number-1].value(0)
    for column_number in columns:
        col_pins[column_number-1].value(1)
        
    utime.sleep(delay)

    row_pins[row_number-1].value(1)
    for column_number in columns:
        col_pins[column_number-1].value(0)
        
def first_task():
    for i in range (300):
        show_row(2, [1, 3, 5], 0.001)
    
def second_task():
    for i in range (300):
        show_row (1, [1, 2, 3, 4, 5], 0.001)
        show_row (2, [1], 0.001)
        show_row (3, [1, ], 0.001)
        show_row (4, [1, 2, 3, 4, 5], 0.001)
        show_row (5, [1,], 0.001)
        show_row (6, [1,], 0.001)
        show_row (7, [1,], 0.001)
        
def third_task():
    for i in range(300):
        show_row (1, [1, 2, 3, 4, 5], 0.001)
        show_row (2, [3], 0.001)
        show_row (3, [3], 0.001)
        show_row (4, [3], 0.001)
        show_row (5, [3], 0.001)
        show_row (6, [3], 0.001)
        show_row (7, [1, 2, 3, 4, 5], 0.001)
        
def main():
    global row_pins, col_pins
    # define row and column pin numbers
    row_pin_numbers = [7, 11, 6, 9, 0, 5, 1]
    col_pin_numbers = [10, 2, 3, 8, 4]

    row_pins = []
    col_pins = []

    # set all the pins as outputs and set column pins high, row pins low
    for row_number in row_pin_numbers:
        row_pins.append(Pin(row_number, Pin.OUT, value = 1))

    for col_number in col_pin_numbers:
        col_pins.append(Pin(col_number, Pin.OUT, value = 0))

    # Sets the waiting time between rows
    wait_time = 0.05

    # Displays image 50 times
#     i = 0
#     while i < 50:
#         col_pins[2].value(1)
#         row_pins[3].value(0)
# 
#         time.sleep(wait_time)
# 
#         col_pins[2].value(0)
#         row_pins[3].value(1)
# 
#         col_pins[1].value(1)
#         col_pins[3].value(1)
# 
#         row_pins[4].value(0)
# 
#         time.sleep(wait_time)
#         
#         col_pins[1].value(0)
#         col_pins[3].value(0)
#         row_pins[4].value(1)
#         
#         i += 1

    first_task()
    second_task()
    third_task()
    
if __name__ == "__main__":
    main()
