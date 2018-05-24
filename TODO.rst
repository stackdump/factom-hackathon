**last updated**

Thu May 24 02:24:09 CDT 2018
----------------------------

WIP
---

* update brython app enhance PetriNet  editor

  * support clickable handles on arcs
  * allow arc creation with > 1 token weight
  * test/fix issue where simulation errors after removing elements from an existing net (tested w/ octoe)

BACKLOG
-------

* enforce Auth via rest API & socketio connections

  * allow end users to bind listeners to specific schema/oid combos

* ACL on schema creation / all RPC commands

* add feature to save petri-net designs

  * require auth to save (on s3? / filesystem)
  * allow user-created schemata

ICEBOX
-------

* remove all other string substitions 

    from ./storage/postgres.py
    in favor of using composable features of psycopg2:
    http://initd.org/psycopg/docs/sql.html#psycopg2.sql.SQL.join
    http://initd.org/psycopg/docs/sql.html#psycopg2.sql.Placeholder

* re-examine use of 'roles' - leveraging inhibitor arcs

  * enhance or remove feature

* consider relocating /index to /editor or /admin

   * also allow api-only mode - to be deployed without editor enabled
