from machine import Pin, PWM
import utime

def main():
    servo_front = PWM(Pin(16))
    servo_front.freq(50)
    servo_front.duty_ns(1500000)
    while True:
        value = int(input("Enter a value: "))
        if value >= 1400000 and value <= 1600000:
            servo_front.duty_ns(value)
        else:
            print("sorry outside range")
            
            
if __name__ == "__main__":
    main()

   


