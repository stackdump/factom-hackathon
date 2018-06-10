#!/usr/bin/env bash

#--------------------
# Demo PetRI requests
#--------------------

API='http://127.0.0.1:8080'
VETID='dr_chery_york_dvm'
PETID='my_pet_uuid'
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

#-----------------------------
# create the factom blockchain
#-----------------------------

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":5,"method":"stream_create","params":["vetchain", "dr_chery_york_dvm"]}'

curl "${API}/api" \
  -H 'content-type: application/json'  \
  --data-binary '{"id":6,"method":"stream_create","params":["petchain", "my_pet_uuid"]}'

#--------------------
# register Pet's RFID
#--------------------

curl "${API}/dispatch/vetchain/dr_chery_york_dvm/update_rfid" \
  -H 'content-type: application/json' \
  --data-binary '{"petchain": "my_pet_uuid", "rfid": "123.456789999999" }'


