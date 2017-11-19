import socket
import sys



def main():
	argc = len(sys.argv)
	if (argc != 3):
		print 'USAGE: python client.py <IP address> <port number>'
		sys.exit()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket
	s.connect((sys.argv[1], int(sys.argv[2]))) #connect to ip and port

# Starts main
if __name__ == "__main__":
    # execute only if run as a script
    main()