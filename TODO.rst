**last updated**
Mon May  7 22:53:45 CDT 2018

porting features from cyclone based project to autobahn/flask

WIP
---

fix/test event dispatch

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
