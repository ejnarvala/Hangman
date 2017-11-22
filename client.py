import socket
import sys
from server import send_msg_pkt
import re
board = []
wrong_letters = []
num_wrong = 0
word_len = 0

#this return true or false if successful and updates game values and prints messages
def receive(socket):
	global board, wrong_letters, num_wrong, word_len
	r = socket.recv(1) #read first byte for msg_flag
	if(len(r) == 0): #check if connection has been closed
		return False
	msg_flag = ord(r) #convert the msg_flag
	while(msg_flag > 0): #read all messages from the client
		server_msg = socket.recv(msg_flag) #read from buffer
		print server_msg #print whats in buffer
		msg_flag = socket.recv(1) #read next flag
		if(len(msg_flag) == 0): #if connection has been closed
			return False
		msg_flag = ord(msg_flag) #convert next flag
	#continue when word_flag is 0 i.e. a control packet
	word_len = ord(socket.recv(1)) #read word length as specified in format
	num_wrong = ord(socket.recv(1)) #read number of wrong guesses
	if word_len > 0: #double check there is a word to read
		board = list(socket.recv(word_len))
	if num_wrong > 0: #double check there are wrong letters to read
		wrong_letters = list(socket.recv(num_wrong))
	return True

#this returns the message packet to use
def receiveMsg(socket):
	r = socket.recv(1)
	if len(r) == 0:
		return ''
	else:
		msg_flag = ord(r)
		if msg_flag == 0:
			return 0
	return socket.recv(msg_flag)

def guess_valid(guess):
	global board
	guess = guess.lower() #lowercase the guess
	if ((not (re.match('^[a-z]*$', guess))) or len(guess) != 1)		:
	#if the guess is not a latter between a and z or the guess is more than one letter
		print 'Error! Please guess one letter.'
		return False
	if((guess in wrong_letters) or (guess in board)):
	#if the guess has been guessed correctly or incorrectly
		print 'Error! Letter '+ str(guess) + ' has been guessed before, please guess another letter.'
		return False
	return True #it is a valid guess


def main():
	global board, wrong_letters, num_wrong, word_len
	argc = len(sys.argv)
	if (argc != 3): #make sure right number of args
		print 'USAGE: python client.py <IP address> <port number>'
		sys.exit()
	try:
		#attempt to connect to the socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket
		s.connect((sys.argv[1], int(sys.argv[2]))) #connect to ip and port
	except socket.error:
		print 'There was an error with connecting!'
		sys.exit()


	#2Player?
	Tplay_msg = receiveMsg(s)
	Tplay_snd = raw_input(Tplay_msg) #print message, ask user for input
	while(Tplay_snd != 'y' and Tplay_snd != 'n'):
		Tplay_snd = raw_input(Tplay_msg) #print message, ask user for input
	if Tplay_snd == 'y':
		send_msg_pkt(s, '2') #send packet with msg_flag(1), data='2'
		print '' #print blank line
	else:
		send_msg_pkt(s, '') #send packet with msg_flag(0)


	#Ready to Start?
	start_msg = receiveMsg(s)
	start_snd = raw_input(start_msg)
	while(start_snd != 'y' and start_snd != 'n'):
		start_snd = raw_input(start_msg)
	if start_snd == 'y':
		send_msg_pkt(s, '')
		print ''
	else:
		s.close()
		sys.exit()

	while(receive(s)):
		print ' '.join(board) #prints board with spaces between the letters/underscores
		print 'Incorrect Guesses: ' + ' '.join(wrong_letters) + '\n' #same as above for wrong guesses
		if ('_' in board and len(wrong_letters) < 6):
			guess = raw_input("Letter to Guess: ").lower() #ask client to guess a letter
			while(not guess_valid(guess)): #keep asking until guess is valid to send
				guess = raw_input("Letter to Guess: ").lower()
			send_msg_pkt(s, guess) #send the guess
	s.close()



# Starts main
if __name__ == "__main__":
    main()
