#!/usr/bin/env bash

#------------------------------------------------
# Demo PetRI requests
#
# This script simulates interaction from a WebUI
#------------------------------------------------

API='http://127.0.0.1:8080'
VETID='testdr_chery_york_dvm'
PETID='testmy_pet_uuid'
RFID='123.456789999999'

#---------------------
# register Pet's RFID
#---------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/update_rfid" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "1528596301409", "rfid": "123.456789999999" }'
