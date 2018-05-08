**last updated**

Sun May  6 13:18:03 CDT 2018

porting features from cyclone based project to autobahn/flask

WIP
---

* test schema creation - currenly invoking rpc api from ipython doesn't work

BACKLOG
-------

* fix/test rpc API

* benchmark & compare w/ cyclone implementation

* fix Websocket connection

ICEBOX
-------

* re-examine use of 'roles' - leveraging inhibitor arcs

* ACL on schema creation / all RPC commands

* add feature to save petri-net designs
  * require auth to save (on s3? / filesystem)
  * allow user-created schemata

* update brython app enhance PetriNet  editor
  * edit update properties on select
  * support clickable handles on arcs
  * allow arc creation with > 1 token weight
