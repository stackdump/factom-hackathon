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

#--------------------
# Destroy existing DB
#--------------------

echo "API: ${API}"

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":1,"method":"schema_destroy","params":["petchain"]}'

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":2,"method":"schema_destroy","params":["vetchain"]}'

#----------------
# Create a new DB
#----------------

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":3,"method":"schema_create","params":["petchain","petchain"]}'

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":4,"method":"schema_create","params":["vetchain","vetchain"]}'

#---------------------------
# create factom blockchains
#---------------------------

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":5,"method":"stream_create","params":["vetchain", "testdr_chery_york_dvm"]}'

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":6,"method":"stream_create","params":["petchain", "testmy_pet_uuid"]}'

#---------------------
# register Pet's RFID
#---------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/update_rfid" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'

#--------------------------------
# start paperwork for Pet travel
#--------------------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/new_travel_process" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'

#----------------------
# first rabies vaccine
#----------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/vaccine" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'

#----------------
# rabies booster
#----------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/booster" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'

#---------------------------
# test vaccines are working
#---------------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/titer_test" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'

#-----------------------------------------
# submit lab works and paperwork to gov't
#-----------------------------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/submit_lab_work" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'

#-----------------------------------
# Verify that all work is completed
#-----------------------------------

curl "${API}/dispatch/vetchain/testdr_chery_york_dvm/verified_complete" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "testmy_pet_uuid", "rfid": "123.456789999999" }'
