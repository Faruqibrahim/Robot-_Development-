import socket
import easygopigo3 as go

myRobot = go.EasyGoPiGo3()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

myRobot.set_speed(150)
def main():
    try:
        # Change port number to 6xyz where xyz is the number of your SD card following the 'R'
        # Use 00z for 1-digit numbers e.g. R4 == 6004, and use 0yz for 2-digit numbers R15 == 6015
        PORT_NR = 6666  # You should change it

        server_socket.bind(('', PORT_NR))

        if PORT_NR == 6666:
            raise ValueError("You did not change the port number to 60xx")

        while True:
            dataFromClient, address = server_socket.recvfrom(256)  # Receive data from client

            # Data is received as a bit stream, so it needs to be decoded first
            dataFromClient = dataFromClient.decode("utf-8").strip()  # To avoid any errors in comparison when a line ending is appended

            print(dataFromClient)  # To see what is received

            if dataFromClient == 'F':
                print("fwd")
                myRobot.forward()

            elif dataFromClient == 'B':
                print("bwd")
                myRobot.backward()

            elif dataFromClient == 'S':
                print("stop")
                myRobot.stop()
            # <-- You should implement the rest of the necessary commands!

    finally:
        # Close the socket if any error occurs
        myRobot.stop()  # Make sure to always stop the robot if the server stops for any reason
        print("exiting")
        server_socket.close()

if __name__ == "__main__":
    main()