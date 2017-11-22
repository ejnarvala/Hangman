# CS3251 Project 2: Hangman - Ejnar Arechavala & Sharan Kumar

#### Single Player
The server side (server.py) takes in arguments for port number and an optional word list file and binds a socket to the localhost and specified port. It runs a while loop that continually listens for connections from any clients (client.py). Upon a succesful connection, a new thread is started on the server side as to keep listening for other connections. The client is then prompted as to whether they are ready for the game, upon which an affirmation tells the server to start the game by creating a new Game object from a random word in the word list. If the client has 3 games running already though, the client will recieve a server-overloaded message and be disconnected. Else, the the client displays the empty board and the client is prompted for a valid, single letter guess (checked on client-side) which is sent to the server for processing and then sent back to the client side with the updated board, which is dependent on the guess being correct. At all times the client can see which 
letters they have guessed correctly/incorrectly and the state of the current board. The client gets 6 incorrect guesses before they lose the game and the connection is ended. If they are able to guess the word, they are congratulated on their win before the connection is terminated.
#### Two Player - Extra Credit
The two player mode is an extension of the single player program. With this version, upon connecting, the first client is asked if they want to play a two player version of the game, and if they select yes, they are asked to wait until another client connects and also selects this two player option. Once a second client connects and selects to play two player, the server will start a game with both clients. If the client declines the option to play the multiplayer mode, they will be directed to the standard single player mode. In the two player version, the two clients alternate guesses and the client whose turn it isn't is told to wait for their partner to make their guess. Both players share penalties and both lose when there is a total of 6 wrong guesses. This server implementation supports a total of 3 concurrent games, where the games can be any combination of single or multiplayer games.

## Authors

  * Ejnar - Socket communication, packet formatting, and game flow
  * Sharan - File I/O, socket initialization/connection, and program initialization. 
  * Both - Program flow, game logic, and testing. 


## Installation/Requirements
  * Python 2.7.12
    * thread
    * socket
    * sys
    * random
    * re

All packages used were standard python library packages

## How to Run
### Start the server
~~~
python server.py <port number> [dictionary file name]
~~~
where [dictionary file name] is an optional input if you want to use a separate text file as the possible words. If left blank, the following default
words are used:
~~~
'jazz', 'buzz', 'mojo','zaps', 'jinx','pizza', 'buffs','jumpy', 'junks', 'hello','puzzle', 'buzzed', 'huzzah', 'clique', 'limpy'
~~~

### Connect clients
~~~
python client.py <IP address> <port number>
~~~

## Example Program Output - Single Player

### Server side


###### Started with
~~~
python server.py 2017
~~~
###### Output
~~~
Server Started! at localhost:2017
Listening for Connections...
Connection Started with ('127.0.0.1', 53286)
Connection Ended with ('127.0.0.1', 53286)
~~~


### Client Side
###### Started with
~~~
python client.py 127.0.0.1 2017
~~~

###### Output
~~~
Ready to start game? (y/n): y

_ _ _ _ _ _
Incorrect Guesses:

Letter to Guess: a
_ _ _ _ _ _
Incorrect Guesses: a

Letter to Guess: b
b _ _ _ _ _
Incorrect Guesses: a

Letter to Guess: u
b u _ _ _ _
Incorrect Guesses: a

Letter to Guess: z
b u z z _ _
Incorrect Guesses: a

Letter to Guess: e
b u z z e _
Incorrect Guesses: a

Letter to Guess: a
Error! Letter a has been guessed before, please guess another letter.
Letter to Guess: i
b u z z e _
Incorrect Guesses: a i

Letter to Guess: d
b u z z e d
Incorrect Guesses: a i

You Win!
Game Over!
~~~


## Example Program Output - Two Player [Extra Credit]

### Server side
###### Started with
~~~
python server.py 2017
~~~
###### Output
~~~
Server Started at localhost:2017
Listening for Connections...
Connection Started with ('127.0.0.1', 64666)
Connection Started with ('127.0.0.1', 64667)
Connection Ended with ('127.0.0.1', 64667)
Connection Ended with ('127.0.0.1', 64666)
~~~
### Client Side - Player 1
###### Started with
~~~
python client.py 127.0.0.1 2017
~~~
###### Output
~~~
Two Player? (y/n): y

Ready to start game? (y/n): y

Waiting for other player!
Game Starting!
Your Turn!
_ _ _ _ _
Incorrect Guesses:

Letter to Guess: a
Correct!
Waiting on other player...
Your Turn!
_ _ _ _ a
Incorrect Guesses: t

Letter to Guess: z
Correct!
Waiting on other player...
Your Turn!
p _ z z a
Incorrect Guesses: t

Letter to Guess: i
Correct!
p i z z a
Incorrect Guesses: t

You Win!
Game Over!
~~~

### Client Side - Player 2
###### Started with
~~~
python client.py 127.0.0.1 2017
~~~
###### Output
~~~
Two Player? (y/n): n
Ready to start game? (y/n): y

_ _ _ _ _
Incorrect Guesses:

Letter to Guess: a
_ _ _ _ a
Incorrect Guesses:

Letter to Guess: bb
Error! Please guess one letter.
Letter to Guess: b
_ _ _ _ a
Incorrect Guesses: b

Letter to Guess: c
_ _ _ _ a
Incorrect Guesses: b c

Letter to Guess: d
_ _ _ _ a
Incorrect Guesses: b c d

Letter to Guess: e
_ _ _ _ a
Incorrect Guesses: b c d e

Letter to Guess: p
p _ _ _ a
Incorrect Guesses: b c d e

Letter to Guess: i
p i _ _ a
Incorrect Guesses: b c d e

Letter to Guess: z
p i z z a
Incorrect Guesses: b c d e

You Win!
Game Over!
~~~








