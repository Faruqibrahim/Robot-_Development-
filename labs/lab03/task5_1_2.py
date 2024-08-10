#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM, ADC
import time
import sys
import select


def handle_input(servo, in_value):
    
    if in_value >= 1400000 and in_value <= 1600000:
        servo.duty_ns(in_value)
    else:
        print("sorry outside range")
    """
    Arguments:
        servo           -- PWM, servo object
        in_value        -- int, input from Shell
    
    Returns:
        nothing
    """
    pass

last_time = 0
def print_50ms(als):
    global last_time
    data = als.read_u16()
    current_time = time.ticks_ms()
    if (current_time >last_time +50):
        #print("data", data)
        last_time = current_time
    pass

shade = True

start_time = 0
def calculate_rpm(als, low_thresh, high_thresh):
    global shade, start_time
    data = als.read_u16()
    
    if data < low_thresh and shade == False:
        #print ("falling ")
        
        current_time = time.ticks_ms()
        period = current_time - start_time
        
        start_time = current_time
        rpm = 60 * 1000 / period
        print(data)
        print(rpm)
        shade = True
        
        
    elif data > high_thresh and shade == True:
        #print("rising")
        shade = False
    
    
    """
    Arguments:
        als              -- ADC, sensor object
        low_thresh       -- int, lower threshold for RPM calculation
        high_thresh      -- int, upper threshold for RPM calculation
    
    Returns:
        nothing    
    """
    pass
    

        
def main():
    servo = PWM(Pin(16))
    servo.freq(50)
    servo.duty_ns(1500000)
    als = ADC(Pin(27, Pin.IN)) # Initialise ALS connection here
    low_thresh = 4000 # Choose a suitable value
    high_thresh = 7000 # Choose a suitable value
   
    while True:
        data_in = select.select([sys.stdin], [], [], 0)[0]
        if not data_in:
            calculate_rpm(als, low_thresh, high_thresh)
            print_50ms(als)
        else:
            line = data_in[0].readline()
            if line.rstrip():
                handle_input(servo, int(line))


if __name__ == "__main__":
    main()

