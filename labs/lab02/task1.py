#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin
import utime

# Defining row pins for ease of use.
# You should enter the GPIO numbers that you connected your display to.
pin_numbers = [1, 0, 2, 13, 15, 12, 14]
pins = []

def init():
    global pins
    
    # Create a list of machine Pin objects and set them to value 1
    for pin_number in pin_numbers:
        pin = Pin(pin_number, Pin.OUT)
        pins.append(pin)
        pin.value(1) # Turn off LED

def main():
    init()
    #set i to 0 for counting 
    i = 0
    current_state = "count up"
    
    while True:
        #first state
        if current_state == "count up":
            if i < 7:
                current_state = "count up"
                pin = pins[i]
                pin.value(0)
                utime.sleep(0.1)
                pin.value(1)
                i += 1
                print(i)
            
            #condition to change state
            elif i == 7:
                current_state = "count down"
                  
        #second state   
        elif current_state == "count down":
            current_state = "count down"
            i -= 1
            pin = pins[i]
            pin.value(0)
            utime.sleep(0.1)
            pin.value(1)
            print(i)
            
            if i == 0:
                current_state = "count up"
    
        pass


if __name__ == "__main__":
    main()
