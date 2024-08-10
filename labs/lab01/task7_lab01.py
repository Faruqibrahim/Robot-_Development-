#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time
import machine
import math
from machine import Pin
import time

echo_pin = 3 # < --- YOU HAVE TO ENTER THE GP<x> PIN, YOU HAVE CONNECTED ECHO TO
trig_pin = 2 # < --- YOU HAVE TO ENTER THE GP<x> PIN, YOU HAVE CONNECTED TRIGGER TO

delay_us = 60 # < --- YOU HAVE TO FIND THE MINIMAL VALUE FROM THE DATASHEET

"""
Datasheet for Ultrasonic Ranging Module HC - SR04
https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
"""

"""
Set the following pins to correct modes!
"""
trigger = Pin(trig_pin, Pin.OUT)
echo = Pin(echo_pin, Pin.IN)


def get_ultrasonic_reading(timeout_us=100_000, default_value=-1):
    method_start_us = time.ticks_us()
    trigger.high()
    time.sleep_us(delay_us)
    trigger.low()
    signal_rise = time.ticks_us()
    signal_fall = signal_rise

    while echo.value() == 0:
        signal_rise = time.ticks_us()
        if time.ticks_diff(signal_rise, method_start_us) > timeout_us:
            return default_value

    while echo.value() == 1:
        signal_fall = time.ticks_us()
        if time.ticks_diff(signal_fall, method_start_us) > timeout_us:
            return default_value

    duration_us = signal_fall - signal_rise

    return duration_us


def get_distance_in_mm(duration_us):
    """
    YOU HAVE TO CALCULATE THE distance_mm BASED ON THE duration_us. FIND THE FORMULA FROM THE DATASHEET AND IMPLEMENT IT HERE
    """
    #The formular below was gotten from the datasheet
    
    distance_from_object_in_mm = duration_us/58*10

    return distance_from_object_in_mm

def main():
        lcd_columns = 16
        lcd_rows = 2
        
        # Replace x with the pin number, board.GPx in CircuitPython is the same as machine.Pin(x) in MicroPython
        scl_pin = board.GP7
        sda_pin = board.GP6
        
        i2c = busio.I2C(scl_pin, sda_pin)
        lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
        
        while True:
            duration_us = get_ultrasonic_reading()
            dist_mm = get_distance_in_mm(duration_us)
            print("The distance from object is:", dist_mm, "mm")
            lcd.message = f"US measurement \n {dist_mm} "
                        
            time.sleep(0.5)
                

if __name__ == "__main__":
    # Run the main function
    main()
