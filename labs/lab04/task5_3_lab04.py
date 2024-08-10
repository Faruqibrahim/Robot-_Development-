import easygopigo3 as go
import time

myRobot = go.EasyGoPiGo3()
def main():
    myRobot.blinker_on(1)
    myRobot.blinker_on(0)
    myRobot.set_speed(300)
    myRobot.drive_cm(45)
    myRobot.steer(150, -150)
    myRobot.blinker_off(1)
    myRobot.blinker_on(0)
    time.sleep(0.2)
    myRobot.orbit(-60, 90)
    myRobot.steer(145, -145)
    myRobot.blinker_on(1)
    myRobot.blinker_off(0)
    time.sleep(0.3)
    myRobot.orbit(50, 55)
    
    myRobot.stop()

if __name__ == "__main__":
    main()

