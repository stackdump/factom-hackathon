import json
from browser import window, document as doc
from browser import websocket, ajax, console

def onload():
    console.log('context loaded')
    """ TODO bind UI events """

class Context(object):

    def __init__(self):
        # TODO load config by getting json file configed in window.Bitwrap.config
        self.seq = 0
        self.endpoint = 'http://127.0.0.1:8080'

    @staticmethod
    def echo(req):
        """ write return value to consoel """
        console.log(req.response)

    @staticmethod
    def clear():
        """ clear python terminal """
        doc['code'].value = ''

    def _rpc(self, method, params=[], callback=None, errback=None):
        """  _rpc(method, params=[], callback=None, errback=None): make JSONRPC POST to backend """
        self.seq = self.seq + 1
        req = ajax.ajax()

        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)

        req.open('POST', self.endpoint + '/api', True)
        req.set_header('content-type', 'application/json')
        req.send(json.dumps({'id': self.seq, 'method': method, 'params': params}))

    def _get(self, resource, callback=None, errback=None):
        """ _get(resource, callback=None, errback=None): make http GET to backend """
        req = ajax.ajax()
        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)
        req.open('GET', self.endpoint + resource, True)
        req.send()

    def schemata(self, callback=None):
        """ schemata(callback=None): retrieve list of available state machine definitions """
        self._get('/schemata', callback=callback)

    def state(self, schema, oid, callback=None):
        """  state(schema, oid, callback=None): get current state """
        self._get('/state/%s/%s' % (schema, oid), callback=callback)

    def machine(self, schema, callback=None):
        """ machine(schema, callback=None): get machine definition """
        self._get('/machine/%s' % schema, callback=callback)

    def dispatch(self, schema, oid, action, payload={}, callback=None):
        """ dispatch(schema, oid, action, payload={}, callback=None): dispatch new event to endpoint  """
        req = ajax.ajax()

        if callback:
            req.bind('complete', callback)
        else:
            req.bind('complete', self.echo)

        req.open('POST', self.endpoint + '/dispatch/%s/%s/%s' % (schema, oid, action), True)
        req.set_header('content-type', 'application/json')
        data = json.dumps(payload)
        req.send(str(data))


    def stream(self, schema, oid, callback=None):
        """ stream(schema, oid, callback=None): get all events """
        self._get('/stream/%s/%s' % (schema, oid), callback=callback)

    def event(self, schema, eventid, callback=None):
        """ event(schema, eventid, callback=None): get a single event """
        self._get('/event/%s/%s' % (schema, eventid), callback=callback)

    def exists(self, schema=None, oid=None, callback=None, errback=None):
        """ exists(schema=None, oid=None, callback=None, errback=None): test for existance of schema and/or stream """

        if not oid:
            self._rpc('schema_exists', params=[schema], callback=callback, errback=errback)
        else:
            self._rpc('stream_exists', params=[schema, oid], callback=callback, errback=errback)

    def load(self, machine_name, new_schema):
        """ load(machine_name, new_schema): load machine definition as db schema """
        self._rpc('schema_create', params=[machine_name, new_schema])

    def create(self, schema, oid):
        """ create(schema, oid): create a new stream """
        self._rpc('stream_create', params=[schema, oid])

    def destroy(self, schema):
        """ destroy(schema): drop from db / destroys a schema and all events """
        self._rpc('schema_destroy', params=[schema])
