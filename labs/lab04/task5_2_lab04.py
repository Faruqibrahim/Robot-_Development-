import easygopigo3 as go
import time

def main():
    myRobot = go.EasyGoPiGo3() 
    myRobot.set_speed(200)
    myRobot.forward()
    time.sleep(1)
    for i in range (3):
        myRobot.right()
        time.sleep(1.7)
        myRobot.forward()
        time.sleep(1)
        myRobot.stop()

if __name__ == "__main__":
    main()
