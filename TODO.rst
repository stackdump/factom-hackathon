**last updated**

Wed May 16 09:13:53 CDT 2018
----------------------------

porting features from cyclone based project to autobahn/flask
refactor GUI using latest brython/jquery/jquery UI/ snap libs

WIP
---
* fix editor commands/buttons

BACKLOG
-------
* fix simulator - update token ledger + will need to get token count from bound element data

* fix/test event dispatch issue where GUI click event doesn't result in a dispatch

* fix Websocket connection 'should use /ws'
  * should route all commits to websocket (for development mode)

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
