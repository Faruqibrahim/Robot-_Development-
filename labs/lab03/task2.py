#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import Pin, PWM
import time

def turn_servo_deg(servo, input_degree):
    pwm_0_deg = 550000
    pwm_180_deg = 2370000
    one_degree = (pwm_180_deg - pwm_0_deg) / 180
    pwm_input = int(pwm_0_deg + (one_degree * input_degree))
    
    servo.duty_ns(pwm_input)
    time.sleep(0.05)


def main():
    servo_front = PWM(Pin(1))
    servo_front.freq(50)
    
    turn_servo_deg(servo_front, 90)


if __name__ == "__main__":
    main()

   
