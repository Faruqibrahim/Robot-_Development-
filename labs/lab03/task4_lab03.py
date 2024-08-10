from machine import Pin, ADC
import time

sensor = ADC(Pin(27, Pin.IN))
led = Pin(25, Pin.OUT)

def main():
    while True:
        data = sensor.read_u16()
        print(data)
        time.sleep(0.1)
        if data < 4000:
            led.high()
            
        else:
            led.low()
            
if __name__ == "__main__":
    main()