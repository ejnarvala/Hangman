import socket
import sys
from server import send_msg_pkt

board = []
wrong_letters = []
num_wrong = 0
word_len = 0
rec_buf = ''
snd_buf = ''


def receive(socket):
	r = socket.recv(1)
	if(len(r) == 0):
		socket.close()
		sys.exit()
	msg_flag = ord(r)
	if (msg_flag == 0):
		word_len = ord(socket.recv(1))
		print word_len
		num_wrong = ord(socket.recv(1))
		print num_wrong
		board = list(socket.recv(word_len))
		print board
		wrong_letters = list(socket.recv(num_wrong-1))
		print wrong_letters
	else:
		rec_buf = socket.recv(msg_flag)
		print rec_buf
	print 'end of receive'
	return True

def guess_valid(guess):
	guess = guess.lower()
	if ((not (re.match('^[a-z]*$', guess))) or len(guess) > 1): #if not a letter
		print 'Error! Please guess one letter.'
		return False	
	if((guess in wrong_letters) or (guess in board)):
		return 'Error! Letter '+ str(guess) + ' has been guessed before, please guess another letter.'
		return False
	return True


def main():
	argc = len(sys.argv)
	if (argc != 3):
		print 'USAGE: python client.py <IP address> <port number>'
		sys.exit()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket
		s.connect((sys.argv[1], int(sys.argv[2]))) #connect to ip and port
	except socket.error:
		print 'There was an error with connecting!'
		sys.exit()

	msg_bytes = ord(s.recv(1)) #read length of first message
	rec_msg = s.recv(msg_bytes) #recieve the message
	snd_msg = raw_input(rec_msg) #print message, ask user for input
	while(snd_msg != 'y' and snd_msg != 'n'):
		snd_msg = raw_input(rec_msg) #print message, ask user for input
	if snd_msg == 'y':
		send_msg_pkt(s, '') #send packet with msg_flag(0)
		print ''
	else:
		s.close()
		sys.exit()

	while(receive(s)):
		print ' '.join(board)
		print 'Incorrect Guesses: ' + ' '.join(wrong_letters)
		guess = raw_input("Letter to Guess: ")
		while(not guess_valid(guess)):
			guess = raw_input("Letter to Guess: ")
		send_msg_pkt(s, guess)


# Starts main
if __name__ == "__main__":
    # execute only if run as a script
    main()