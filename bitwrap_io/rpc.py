"""
rpc api - provides schema & stream CRUD
"""
import bitwrap_io
import bitwrap_io.config
import bitwrap_io.machine as pnml
from bitwrap_io.storage import postgres

from petfax import factom

SETTINGS = bitwrap_io.config.options()

def call(method, params):
    """ invoke rpc method """
    return globals()['rpc_' + method](*params)

def eventstore(schema):
    """ open eventstore on bitwrap storage """
    return bitwrap_io.open(schema, **SETTINGS)

def rpc_schema_exists(schema):
    """ test that an event-machine schema exists """
    return eventstore(schema).storage.db.schema_exists()

def rpc_schema_create(schema, name):
    """ create event-machine as database schema """
    machine = pnml.Machine(schema)

    try:
        postgres.create_schema(machine, schema_name=name, **SETTINGS)
    except Exception as ex:
        print(ex)

    return rpc_schema_exists(name)

def rpc_schema_destroy(schema):
    """ drop database schema """
    postgres.drop_schema(schema, **SETTINGS)

def rpc_stream_exists(schema, oid):
    """ test that a stream exists """
    return eventstore(schema).storage.db.stream_exists(oid)

    return res

def rpc_stream_create(schema, oid):
    """ create a new stream and a corresponding blockchain on factom """ 

    res = eventstore(schema).storage.db.create_stream(oid)

    if 'chain' not in schema:
        # KLUDGE only create factom blockchain if name contains 'chain'
        return res


    # TODO: create blockchain and capture data as payload
    print('create blockchain for %s:%s' % (schema, oid))

    payload = '{}'

    res = eventstore(schema)(oid=oid, action='create_chain', payload=payload)
    # TODO: trigger 'create_chain' action & store chain_id to payload
    return res
