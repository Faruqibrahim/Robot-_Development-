#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM
import utime

pwm = PWM(Pin(22))
pwm.freq(50)

def turn_servo_deg(input_degree):
    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))
    
    pwm.duty_ns(pwm_input)

def main():
    #in this loop turn the servo to apply bfeaks for 2secs and disengage breaks for 1sec
    while True:
        turn_servo_deg(10)
        utime.sleep(2)
        turn_servo_deg(180)
        utime.sleep(1)


if __name__ == "__main__":
    # Run the main function
    main()

   
