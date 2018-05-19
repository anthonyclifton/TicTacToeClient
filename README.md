# A game client for m,n,k games like Tic-Tac-Toe

M,n,k games beyond the simplest 3,3,3 version most people played as children
are largely of mathematical interest.  However, as they become more larger
and especially if you start playing in dimensions > 2, tactics and strategy
can become very important.

You can read more about tic-tac-toe like games at:
[Wikipedia](https://en.wikipedia.org/wiki/M,n,k-game)

This game client is designed to be autonomous.  It runs in of three modes by executing
the supplied scripts after you've configured the client to talk to a server.

Because the server uses webhook calls back to the client, it's important that the
client and server be able to reach each other for http requests (both directions).
If they're on opposite sides of NAT's, firewalls, etc then it's likely the server
will be unable to make requests back to the client.

## Installation

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
