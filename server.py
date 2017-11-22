import socket
import thread
import sys
import random

open_games = 0
running_games = 0
players_waiting = []
#default word list is
words = ['jazz', 'buzz', 'mojo','zaps', 'jinx',
	'pizza', 'buffs','jumpy', 'junks', 'hello',
	'puzzle', 'buzzed', 'huzzah', 'clique', 'limpy']

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
			return True
		else:
			self.wrong_letters.append(letter)
			if len(self.wrong_letters) == 6:
				self.game_over = True
			return False


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
	r = socket.recv(1) #read first byte (msg_flag)
	if(len(r) == 0): #if nothing, client has disconnected, noted by empty string
		return ''
	else:
		#get msg_flag and read that amount from socket
		msg_flag = ord(r)
		if(msg_flag == 0):
			return msg_flag #theoretically should only be the start_msg from client
		else:
			return socket.recv(msg_flag)


def run_game(socket, g):
	connected = True #for seeing if client disconnected
	while((not g.game_over) and connected): #while game running
		send_ctrl_pkt(socket, g) #send it current state of the game
		msg = receive_msg_pkt(socket) #wait for response i.e the guess
		#print msg
		if(len(msg) == 0): #if disconnected
			connected = False
		else:
			g.guess(msg)
	if connected: #if still connected when game ends/disconnects
		#send game packets
		send_ctrl_pkt(socket, g)
		if (g.game_won):
			send_msg_pkt(socket, 'You Win!')
		else:
			send_msg_pkt(socket, 'You Lose!')
		send_msg_pkt(socket, 'Game Over!')

def run_game_Tplayer(p1_socket, p2_socket, g):
	connected = True
	send_msg_pkt(p1_socket, 'Game Starting!')
	send_msg_pkt(p2_socket, 'Game Starting!')
	turn = False
	while((not g.game_over) and connected):
		if(turn):
			socket1 = p1_socket
			socket2 = p2_socket
		else:
			socket1 = p2_socket
			socket2 = p1_socket
		send_msg_pkt(socket2, 'Waiting on other player...')
		send_msg_pkt(socket1, 'Your Turn!')
		send_ctrl_pkt(socket1, g)
		msg = receive_msg_pkt(socket1)
		if(len(msg) == 0):
			connected = False
		else:
			if(g.guess(msg)):
				send_msg_pkt(socket1, 'Correct!')
			else:
				send_msg_pkt(socket1, 'Wrong!')
		turn = not turn #switch players
	if connected:
		send_ctrl_pkt(socket1, g)
		send_ctrl_pkt(socket2, g)
		if (g.game_won):
			send_msg_pkt(p1_socket, 'You Win!')
			send_msg_pkt(p2_socket, 'You Win!')
		else:
			send_msg_pkt(p1_socket, 'The word was ' + ''.join(g.word))
			send_msg_pkt(p2_socket, 'The word was ' + ''.join(g.word))
			send_msg_pkt(p1_socket, 'You Lose!')
			send_msg_pkt(p2_socket, 'You Lose!')
		send_msg_pkt(p1_socket, 'Game Over!')
		send_msg_pkt(p2_socket, 'Game Over!')
	print 'Connection Ended with', p1_socket.getpeername()
	print 'Connection Ended with', p2_socket.getpeername()
	p2_socket.close()
	p1_socket.close()


def on_new_client(socket, addr):
	global running_games, open_games
	#when new client connected, ask to start game
	send_msg_pkt(socket,'Two Player? (y/n): ')
	start_msg = receive_msg_pkt(socket)
	if int(start_msg) == 2: #if two player mode
		send_msg_pkt(socket,'Ready to start game? (y/n): ')
		start_msg = receive_msg_pkt(socket)
		if start_msg == 0:
			if(running_games >= 3): #if 3 or more games already running
				send_msg_pkt(socket, 'Server-Overloaded') #then close connection
				socket.close()
				print 'Connection Ended with', addr
			else:
				if open_games == 0: #if there are no open games, make new one
					open_games += 1
					players_waiting.append(socket)
					send_msg_pkt(socket, 'Waiting for other player!')
				else:
					running_games += 1 #only increment count once game has started
					open_games -= 1
					run_game_Tplayer(socket, players_waiting.pop(),Game(random.choice(words)))
					running_games -= 1 #whenever game is finnished running
		else:
			socket.close()
			print 'Connection Ended with', addr

	elif start_msg == 0: #if not 2 player mode, start 1 player mode
		send_msg_pkt(socket,'Ready to start game? (y/n): ')
		start_msg = receive_msg_pkt(socket)
		if start_msg == 0: #if it is a packet with msg_flag of 0
			if(running_games >= 3): #if 3 or more games already running
				send_msg_pkt(socket, 'Server-Overloaded') #then close connection
			else:
				#start a new game
				g = Game(random.choice(words))
				running_games += 1
				run_game(socket, g) #run game g
				running_games -= 1 #whenever game is finnished running
		socket.close()
		print 'Connection Ended with', addr





def main():
	global words #declare global words to modify
	argc = len(sys.argv) #number of arguments passed in
	if (argc != 2 and argc != 3):
		print 'USAGE: python server.py <port number> [dictionary file name]'
		sys.exit()
	if(argc == 3): #if 3 args, read the third which will be text file name
	#overwrite default word list
		with open(sys.argv[2]) as f:
			words = f.read().splitlines()[1:] #read lines into list
	host = 'localhost' # start on 127.0.0.1, 'localhost' is an optimization
	port = int(sys.argv[1]) #port number from input
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create new socket
	s.bind((host, port)) #bind host and port
	print 'Server Started at ' + str(host) + ":" + str(port)
	s.listen(5) #listen for connections
	print 'Listening for Connections...'
	while True: #listen forever
		client, addr = s.accept()     # Establish connection with client.
		print 'Connection Started with', addr
		thread.start_new_thread(on_new_client,(client,addr)) #start new thread with client socket
	s.close()

# Starts main
if __name__ == '__main__':
	 main()
