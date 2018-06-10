"""
rpc api - provides schema & stream CRUD
"""
import json

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

def _machine_def(schema):
    """ return json blob with petri-net state machine def """
    machine = pnml.Machine(schema)
    res = {
        'machine': {
            'name': schema,
            'places': machine.net.places,
            'transitions': machine.net.transitions
        }
    }

    return json.dumps(res)

def rpc_stream_create(schema, oid):
    """
    create a new stream and a corresponding blockchain on factom
    each blockchain contains full state machine def
    """ 

    res = eventstore(schema).storage.db.create_stream(oid)

    if 'chain' not in schema:
        # KLUDGE only create factom blockchain if name contains 'chain'
        return res


    print('create blockchain for %s:%s' % (schema, oid))
    fact_res = factom.create_chain(external_ids=[schema, str(oid)], content=_machine_def(schema))

    _payload = json.dumps(fact_res)

    res = eventstore(schema)(oid=oid, action='create_chain', payload=json.dumps(fact_res))

    res['action'] = 'create_chain'
    res['payload'] = _payload

    return res
