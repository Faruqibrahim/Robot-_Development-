from helper.Commander import *

# <-- IP_ADRESS: Your raspberry IP address (You can check it by using 'ip a' command on raspberry terminal)
# <-- PORT_NR: Change port number to 6xyz where xyz is the number of your SD card following the 'R'. Use 00z for 1-digit numbers e.g. R4 == 6004, and use 0yz for 2-digit numbers R15 == 6015
IP_ADDRESS = "your.pi.ip.addr"  # for example "192.168.15.23"
PORT_NR = 6666


def main():

	commander = Commander(IP_ADDRESS, PORT_NR)

	try:
		while True:
			command = input("Enter command (F - forward, B - backward, S - stop, Q - quit) :")
			if command.strip() == 'Q':
				break

			commander.sendCommand(command)

	finally:
		commander.closeSocket()

if __name__ == "__main__":
	main()