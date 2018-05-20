**last updated**

Thu May 17 23:28:04 CDT 2018
----------------------------

porting features from cyclone based project to autobahn/flask
refactor GUI using latest brython/jquery/jquery UI/ snap libs

WIP
---

implementing socketio for notify events

BACKLOG
-------

github auth doesn't work currently:

    RecursionError: maximum recursion depth exceeded while calling a Python object

* provide 2 application configurations development & production modes
  * development listens to all websocket events
  * production is bound by session


ICEBOX
-------
* build a websocket dispatcher/session manager
  * allow end users to bind listeners to specific schema/oid combos

* ACL on schema creation / all RPC commands

* add feature to save petri-net designs
  * require auth to save (on s3? / filesystem)
  * allow user-created schemata

* update brython app enhance PetriNet  editor
  * should install via bitwrap-ui python package
  * edit update properties on select
  * support clickable handles on arcs
  * allow arc creation with > 1 token weight

* remove all other string substitions from ./storage/postgres.py
  in favor of using composable features of psycopg2 :
  http://initd.org/psycopg/docs/sql.html#psycopg2.sql.SQL.join
  http://initd.org/psycopg/docs/sql.html#psycopg2.sql.Placeholder

* allow users to run only the API serving w/ twisted (production mode)
  * consider making the editor into an Admin UI

* re-examine use of 'roles' - leveraging inhibitor arcs
  * enhance or remove feature
