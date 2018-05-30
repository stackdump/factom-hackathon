**last updated**

Wed May 30 07:52:17 CDT 2018
----------------------------

WIP
---

* update brython app enhance PetriNet  editor

  * support clickable handles on arcs
  * allow arc creation with > 1 token weight

BACKLOG
-------

* ACL on schema creation / all RPC commands
* upload new schemata & convert to pnml from editor with 'save' button

* consider if we need to refactor github auth to make it optional
  * use case is: I want to host an API server to just use JWT bearer tokens

ICEBOX
-------

* fork to create gitwrap.com - hosted editing and testing of petri-nets

  * enforce Auth via rest API & socketio connections
  * allow user-created schemata - ( saved in db or s3 )
  * add feature to save petri-net designs
  * require auth to save (on s3? / filesystem)
  * no guarenteed db storage (maybe publish events to s3 bucket)
  * allow end users to bind listeners to specific schema/oid combos
  * POC feature to save petri-net designs (no auth)

* remove all other string substitions 

    from ./storage/postgres.py
    in favor of using composable features of psycopg2:
    http://initd.org/psycopg/docs/sql.html#psycopg2.sql.SQL.join
    http://initd.org/psycopg/docs/sql.html#psycopg2.sql.Placeholder

* re-examine use of 'roles' - leveraging inhibitor arcs

  * enhance or remove feature

