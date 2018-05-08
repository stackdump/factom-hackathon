"""
bitwrap_io

usage:

    import bitwrap_io
    m = bitwrap_io.open('counter')
    m(oid='foo', action='INC', payload={}) # dispatch an event

"""
import sys
import bitwrap_psql as psql

_STORE = {}

class EventStore(object):
    """ bitwrap_io.EventStore """

    def __init__(self, schema, **kwargs):
        self.schema = schema.__str__()
        self.storage = psql.Storage(self.schema, **kwargs)

    def __call__(self, **request):
        """ execute a transformation """
        return self.storage.commit(request)

def open(schema, **kwargs):
    """ open an evenstore by providing a schema name """

    if not schema in _STORE:
        _STORE[schema] = EventStore(schema, **kwargs)

    return _STORE[schema]
