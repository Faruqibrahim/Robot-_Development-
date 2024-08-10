#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# First you need to import the LCD libraries that you just uploaded
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time

def main():
    lcd_columns = 16 # How many characters we can fit on the screen
    lcd_rows = 2     # How many rows of characters we have

    # Replace x with the pin number, board.GPx in CircuitPython is the same as machine.Pin(x) in MicroPython
    scl_pin = board.GP5
    sda_pin = board.GP4

    i2c = busio.I2C(scl_pin, sda_pin)
    # Initialize the LCD
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    while True:
        # Print out statuses of buttons. The variables contain a boolean value (True/False)
        print("LEFT button status: ", lcd.left_button)
        print("RIGHT button status: ", lcd.right_button)
        
        if lcd.right_button == True:
            #add  just space to solve the problem of flickering
            lcd.message = "   "
        else:
            lcd.message = "not pressed"
            
            #lcd.clear()
            

if __name__ == "__main__":
    main()