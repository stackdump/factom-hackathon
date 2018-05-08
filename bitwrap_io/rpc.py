"""
rpc api - provides schema & stream CRUD
"""
import bitwrap_io
import bitwrap_io.config
import bitwrap_psql.postgres as pgsql
import bitwrap_machine as pnml

SETTINGS = bitwrap_io.config.options()

def call(method, params):
    return globals()['rpc_' + method](*params)

def eventstore(schema):
    """ open eventstore on bitwrap storage """
    return bitwrap_io.open(schema, **SETTINGS)

def rpc_schema_exists(schema):
    """ test that an event-machine schema exists """
    return eventstore(schema).storage.db.schema_exists()

def rpc_schema_create(schema, *args):
    """ test that an event-machine schema exists """
    machine = pnml.Machine(schema)

    if args[0] is None:
        name = schema
    else:
        name = args[0]

    try:
        pgsql.create_schema(machine, schema_name=name, **SETTINGS)
    except:
        pass

    return rpc_schema_exists(name)

def rpc_schema_destroy(schema):
    """ test that an event-machine schema exists """
    pgsql.drop_schema(schema, **SETTINGS)

def rpc_stream_exists(schema, oid):
    """ test that a stream exists """
    return eventstore(schema).storage.db.stream_exists(oid)

def rpc_stream_create(schema, oid):
    """ create a new stream if it doesn't exist """
    return eventstore(schema).storage.db.create_stream(oid)
