import socket
import thread
import sys
import random
import re
runnings_games = 0
words = [] #word dictionary

class Game(object):
	def __init__(self, word):
		self.word = list(word.lower()) #list to make easy to change, use .join(word) to make nice
		self.wrong_letters = [] #len of this is #penalties
		self.board = list(("_ "*len(word))[:-1]) #make board, remove trailing space
		print self.board

	def guess(self, letter):
		if (not (re.match('^[A-Za-z]*$', letter))) or len(letter) > 1: #if not a letter
			return 'Error! Please guess one letter.'
		letter = letter.lower() #lowercase letter
		if(letter in self.wrong_letters):
			return 'Error! Letter A has been guessed before, please guess another letter.'
		if(letter in self.word): #if letter is correct guess
			indices = [i for i, a in enumerate(self.word) if a == letter]
			for i in indices:
				print self.word[i]
			for i in indices:
				self.board[2*i] = letter
			if not ('_' in board): #if game is won
				return 'You Win!'
			print self.board
		else:
			self.wrong_letters.append(letter)
			if len(wrong_letters) == 6:
				#TODO: handle destroying game or message to do so
				print "GAME OVER"



def on_new_client(clientsocket,addr):
	global runnings_games
	mygame = Game(random.choice(words))
	if (runnings_games >= 3):
		print 'SERVER OVERLOADED'
		#TODO: server overload code
	else:
		runnings_games += 1
	# while True:
		# msg = clientsocket.recv()
		#do some checks and if msg == someWeirdSignal: break:
		# print addr, ' >> ', msg
		# msg = raw_input('SERVER >> ') 
		#Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
		# clientsocket.send(msg) 
	clientsocket.close()

def main():
	global words #declare global words to modify
	argc = len(sys.argv) #number of arguments passed in
	if (argc != 2 and argc != 3):
		print 'USAGE: python server.py <port number> [dictionary file name]'
		sys.exit()
	if(argc == 3):
		with open(sys.argv[2]) as f:
			words = f.read().splitlines()[1:] #read lines into list
	else: #argc == 2, use default word dictionary
		words = ['jazz', 'buzz', 'hajj', 'fizz', 'jinx', 'huff', 'buff', 'jiff', 'junk', 'quiz']
	host = 'localhost' # start on 127.0.0.1
	port = int(sys.argv[1]) #port number from input
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket
	s.bind((host, port)) #bind host and port
	print 'Server Started!'
	print 'Host:', host, "| Port:", port
	s.listen(5) #listen for connections
	print 'Listening for Connections...'
	while True:
		c, addr = s.accept()     # Establish connection with client.
		print 'Got connection from', addr
		thread.start_new_thread(on_new_client,(c,addr)) #start new thread with client socket
	s.close()




# Starts main
if __name__ == '__main__':
	 main()
