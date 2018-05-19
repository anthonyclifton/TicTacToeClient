# A game client for m,n,k games like Tic-Tac-Toe

M,n,k games beyond the simplest 3,3,3 version most people played as children
are largely of mathematical interest.  However, as they become more larger
and especially if you start playing in dimensions > 2, tactics and strategy
can become very important.

You can read more about tic-tac-toe like games at:
[Wikipedia](https://en.wikipedia.org/wiki/M,n,k-game)

This game client is designed to be autonomous.  It runs in of three modes by executing
the supplied scripts after you've configured the client to talk to a server.
It can operate in player-vs-player mode by having one client execute the `./create`
script, and another execute the `./join [uuid-key]` command that the first will
supply in its output.  In the final mode, you can enter the tournament lobby on the
server by executing `./lobby`.  Your client will then wait for the tournament to
start and play games under direction of the server.

Because the server uses webhook calls back to the client, it's important that the
client and server be able to reach each other for http requests (both directions).
If they're on opposite sides of NAT's, firewalls, etc then it's likely the server
will be unable to make requests back to the client.

## Getting the Software and its Dependencies

* Install homebrew (or equivalent package manager on windows or linux)
  * Mac OSX
    * https://brew.sh/
    * `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
  * `brew install python@2`
* The following is only necessary if you want to maintain separate python environments for dependencies
  * `brew install pyenv`
  * `brew install pyenv-virtualenv`
* `git clone git@github.com:anthonyclifton/TicTacToeClient.git t3client`
* If you want to play with the server you can check it out:
  * `git clone git@github.com:anthonyclifton/n-dimensional-tic-tac-toe.git t3server`
* The following is only necessary if you want to maintain separate python environments for dependencies
  * `cd t3client`
  * `pyenv install 2.7.13`
  * `pyenv virtualenv 2.7.13 t3client`
  * `pyenv local t3client`
  * `pyenv local` (to verify you're using the environment you specified)
* `pip install -Ur requirements.txt` (should download lots of fun dependencies)

## Editing the Configuration File

* You will find a file called `configuration.py` in `tictactoeclient` in the project folder
* Set the server base url.  It will look something like this:
`SERVER_BASE_URL = 'http://localhost:3334'`
* Get your external ip address using something like `ifconfig en0` and look for the `inet` value
* Edit your client's host so it looks something like this: `CLIENT_UPDATE_HOST = 'X.X.X.X'`
where `X.X.X.X` is the value from `inet` in the previous step
* Edit the game name to use when you create a game: `CREATE_GAME_NAME = 'GREETINGS PROFESSOR FALKEN'`
* Edit the player name to use when creating a game: `CREATE_PLAYER_NAME = 'JOSHUA'`
* Edit the player name to use when joining or entering the lobby:
`JOIN_PLAYER_NAME = 'LIGHTMAN'`

## Game Flow

* Player versus Player Mode
  * Execute `./create` on a client to create a new game
  * The create client sends an http post the game server, notifying it that a new
  game should be started.
  * The server responds with the empty game object (no moves yet).
  * The create client starts a web server so it can listen for game updates.
  * Execute `./join [game-uuid-key]` on another client to the join that game.
  When you create a game it will provide output with the join command followed by
  the relevant game key
  * The join client sends an http post to the game server, notifying it that it
  wants to join the game created by the create client.
  * The server responds with the empty game object (no moves yet).
  * The join client starts a web server so it can listen for game updates.
  * The server sends an http post to the create client with the game object.
  * The create client responds with its move after analyzing the board.
  * The server sends an http post to the join client with the game object and
  the create client's move.
  * (Note that the create client always plays X and the join client always plays O).
  * The server continues back and forth, sending updates to the clients and receiving
  the client's move as the response.
  * This continues until the board is full or the game is won, in which case final
  game updates are sent to both clients with the value of the `state` key set to 4
  (or GAME_COMPLETED).  While in the play the `state` is set to 1 (or GAME_INPROGRESS).
* Tournament Mode
