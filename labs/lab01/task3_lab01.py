from machine import Pin
import time

led = Pin(25, Pin.OUT)

def main():
    while True:
        led.high()      # Or all combined:
        time.sleep(1)   # led.toggle()
        led.low()       # time.sleep(1)
        time.sleep(1)   #

if __name__ == "__main__":
    #Run the main function
    main()
