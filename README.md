# Bitwrap-io

A state-machine eventstore 'blockchain style'.

Using Markov chains stored in a Postgres database.

Read the whitepaper [Solving 'State Exposion' with Petri-Nets and Vector Clocks](https://github.com/bitwrap/bitwrap-io/blob/master/whitepaper.md)

### Status

Currently re-writing to be fully async using txpostgres & twisted Klein framework.

Gave up on using autobahn for websockets couldn't cleanly integrate w/ blocking calls from flask w/ async calls to websocket.

Ported Python2 -> Python3 using [Autobahn](http://autobahn.readthedocs.io/en/latest/)
/[Flask](http://flask.pocoo.org/)

[Brython](https://www.brython.info/static_doc/en/intro.html) Web UI is mostly complete.


### Features

**Work-in-Progress**

* Visual State machine designer *does not yet save back to server*
* Eventstore using a relational DB
* Websocket support for observing event streams
