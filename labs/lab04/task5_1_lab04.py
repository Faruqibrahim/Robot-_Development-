import easygopigo3 as go
import time

def main():
    myRobot = go.EasyGoPiGo3() 
    for i in range (5):
        myRobot.set_speed(600)
        myRobot.forward()  
        time.sleep(1)
        myRobot.backward()  
        time.sleep(1)
        myRobot.stop()

if __name__ == "__main__":
    main()