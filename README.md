# Hangman Game

### CS3251 Project 2 - Ejnar Arechavala & Sharan Kumar

The server side (server.py) is a while loop that continually listens for connections from the client side (client.py). Upon a succesful
connection, the client is asked if they want to play a two player version of the game, and if they select yes, they are asked to wait until
another client connects and also selects this two player option. If the client declines the option to play the multiplayer mode, they will be directed to
the standard single player mode. The client is prompted as to whether they are ready for the game, upon which an affirmation starts the game
and displays the empty board. This server implementation supports a total of 3 concurrent games, where the games can be any combination
of single or multiplayer games. The client side is prompted for a valid, single letter guess which is sent to the server for processing and 
then sent back to the client side with the updated board, which is dependent on the guess being correct. At all times the client can see which 
letters they have guessed correctly and the state of the current board. The client gets 6 incorrect guesses before they lose the game and the connection is ended. If they are able to guess the word, they are congratulated on their win before 
the connection is terminated. In the two player version, the two clients alternate guesses and the client whose turn it isn't is told to wait
for their partner to make their guess. 

Ejnar was responsible for socket communication, packet formatting, and game flow while Sharan did file I/O, socket initialization/connection, and program initialization. 
Both members worked on program flow, game logic, and testing. The python version was 2.7.12 and python libraries socket,
thread, sys, random, and re were used.

The program has the following usage for the client side: 
~~~
python client.py <IP address> <port number>
~~~

and the following usage for the server side:
~~~
python server.py <port number> [dictionary file name]
~~~

where [dictionary file name] is an optional input if you want to use a separate text file as the possible words. If left blank, the following default
words are used:
~~~
'jazz', 'buzz', 'mojo','zaps', 'jinx','pizza', 'buffs','jumpy', 'junks', 'hello','puzzle', 'buzzed', 'huzzah', 'clique', 'limpy'
~~~

Here is an example of what the multiplayer program flow would look like for a server and two clients:

server side
~~~
python server.py 2017
Server Started at localhost:2017
Listening for Connections...
Connection Started with ('127.0.0.1', 64666)
Connection Started with ('127.0.0.1', 64667)
Connection Ended with ('127.0.0.1', 64667)
Connection Ended with ('127.0.0.1', 64666)
~~~
first client side
~~~
python client.py 127.0.0.1 2017
Two Player? (y/n): y

Ready to start game? (y/n): y

Waiting for other player!
Game Starting!
Your Turn!
_ _ _ _ _ _
Incorrect Guesses:

Letter to Guess: a
Wrong!
Waiting on other player...
Your Turn!
_ _ _ _ _ e
Incorrect Guesses: a

Letter to Guess: l
Correct!
Waiting on other player...
Your Turn!
p _ _ _ l e
Incorrect Guesses: a

Letter to Guess: i
Wrong!
Waiting on other player...
Your Turn!
p _ _ _ l e
Incorrect Guesses: a i m

Letter to Guess: o
Wrong!
Waiting on other player...
Your Turn!
p u _ _ l e
Incorrect Guesses: a i m o

Letter to Guess: r
Wrong!
Waiting on other player...
You Win!
Game Over!
~~~

second client side
~~~
python client.py 127.0.0.1 2017
Two Player? (y/n): y

Ready to start game? (y/n): y

Game Starting!
Waiting on other player...
Your Turn!
_ _ _ _ _ _
Incorrect Guesses: a

Letter to Guess: 42
Error! Please guess one letter.
Letter to Guess:
Error! Please guess one letter.
Letter to Guess: e
Correct!
Waiting on other player...
Your Turn!
_ _ _ _ l e
Incorrect Guesses: a

Letter to Guess: p
Correct!
Waiting on other player...
Your Turn!
p _ _ _ l e
Incorrect Guesses: a i

Letter to Guess: m
Wrong!
Waiting on other player...
Your Turn!
p _ _ _ l e
Incorrect Guesses: a i m o

Letter to Guess: u
Correct!
Waiting on other player...
Your Turn!
p u _ _ l e
Incorrect Guesses: a i m o r

Letter to Guess: z
Correct!
You Win!
Game Over!
~~~








