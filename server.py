import socket
import thread
import sys
import random

running_games = 0
words = [] #word dictionary

class Game(object):
	def __init__(self, word):
		self.word = list(word.lower()) #list to make easy to change, use .join(word) to make nice
		self.wrong_letters = [] #len of this is #penalties
		self.board = list(("_"*len(word))) #make board, remove trailing space
		self.game_won = False
		self.game_over = False

	def guess(self, letter):
		if(letter in self.word): #if letter is correct guess
			indices = [i for i, a in enumerate(self.word) if a == letter]
			for i in indices:
				self.board[i] = letter
			if not ('_' in self.board): #if game is won
				self.game_won = True
				self.game_over = True
		else:
			self.wrong_letters.append(letter)
			if len(self.wrong_letters) == 6:
				self.game_over = True

def send_ctrl_pkt(socket, game):
	msg_flag = chr(0)
	word_len = chr(len(game.word))
	num_incorrect = chr(len(game.wrong_letters))
	data = msg_flag + word_len + num_incorrect + ''.join(game.board) + ''.join(game.wrong_letters)
	n = socket.send(data)
	# print n, "bytes sent"

def send_msg_pkt(socket, data):
	msg_flag = chr(len(data))
	n = socket.send(msg_flag+data)
	# print n, "bytes sent"

def receive_msg_pkt(socket):
	r = socket.recv(1)
	if(len(r) == 0):
		return ''
	else:
		msg_flag = ord(r)
		return socket.recv(msg_flag)


def run_game(socket, g):
	connected = True
	while(not g.game_over):
		send_ctrl_pkt(socket, g)
		msg = receive_msg_pkt(socket)
		if(len(msg) == 0): #if disconnected
			connected = False
		g.guess(msg)
	if connected:
		if (g.game_won):
			send_msg_pkt(socket, 'You Win!')
		else:
			send_msg_pkt(socket, 'You Lose!')
		send_msg_pkt(socket, 'Game Over!')



def on_new_client(socket, addr):
	global running_games
	send_msg_pkt(socket,'Ready to start game? (y/n): ')
	rec_msg = socket.recv(1)
	if len(rec_msg) != 0:
		rec_msg = ord(rec_msg)
		if(rec_msg == 0): #if recieve packet with msg_flag = 0
			if(running_games >= 3):
				send_msg_pkt(socket, 'Server-Overloaded') #then close connection
			else:
				g = Game(random.choice(words))
				print 'New Game Started!'
				running_games += 1
				run_game(socket, g)
				running_games -= 1 #whenever game is finnished running
	socket.close()
	print 'Connection Ended with', addr


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
		words = ['jazz', 'buzz', 'hajj', 'fizz', 'jinx', 'huffs', 'buffs', 'jiffs', 'junks', 'hello', 'puzzle', 'buzzed', 'huzzah', 'fizzed', 'jumped']
	host = 'localhost' # start on 127.0.0.1
	port = int(sys.argv[1]) #port number from input
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket
	s.bind((host, port)) #bind host and port
	print 'Server Started! at ' + str(host) + ":" + str(port)
	s.listen(5) #listen for connections
	print 'Listening for Connections...'
	while True:
		client, addr = s.accept()     # Establish connection with client.
		print 'Got connection from', addr
		thread.start_new_thread(on_new_client,(client,addr)) #start new thread with client socket
	s.close()

# Starts main
if __name__ == '__main__':
	 main()
