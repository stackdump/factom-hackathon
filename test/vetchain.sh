#!/usr/bin/env bash

#--------------------
# Demo PetRI requests
#--------------------

API='http://127.0.0.1:8080'

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":1,"method":"stream_create","params":["petchain",1528586638118]}'

curl "${API}/dispatch/petchain/1528586638118/update_rfid" \
  -H 'content-type: application/json' \
  --data-binary '{"hello": "world"}'
