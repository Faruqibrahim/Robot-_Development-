#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM
import time

pump_switch = Pin(15, Pin.OUT, value=0)
valve_switch = Pin(14, Pin.OUT)

def turn_servo_deg(servo, input_degree):
    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))
    
    servo.duty_ns(pwm_input)
    time.sleep(0.05)
    
def front_servo(deg):
    servo_front = PWM(Pin(0))
    servo_front.freq(50)
    
    turn_servo_deg(servo_front, deg)
    
def back_servo(deg):
    servo_back = PWM(Pin(1))
    servo_back.freq(50)
    
    turn_servo_deg(servo_back, deg)


def main():
    pump_switch.value(1)
    while True:
        back_servo(0)
        #apply breaks to servo
        front_servo(110)
        time.sleep(1)
        valve_switch.value(1)
        time.sleep(2)
        
        front_servo(0)
        #apply breaks to servo
        back_servo(110)
        time.sleep(1)
        valve_switch.value(0)
        time.sleep(2)
if __name__ == "__main__":
    main()

   

