import re
import json
from browser import window, document as doc
from browser import websocket, ajax, console

_SEQ = 0
_CFG = None
_ENDPOINT = ''
_WS = None

UI_ELEMENT='#code'

def __onload(config):
    """
    config is requested and this method is
    called as this module is included  (see bottom of file)
    """
    global _CFG
    global _ENDPOINT
    global _WS
    _CFG = config
    _ENDPOINT = _CFG['endpoint']

    if 'use_websocket' not in _CFG or not _CFG['use_websocket']:
        return

    # FIXME Error during WebSocket handshake: Unexpected response code: 200
    _WS = websocket.WebSocket(re.sub(r'^http', 'ws', window.location.origin))

    def _open(evt):
        console.log(evt)
        subscribe('brython', 'fswatch')
        window.jQuery(UI_ELEMENT).trigger('init', evt)

    def _error(evt):
        console.log(evt)

    def _message(msg):
        event = json.loads(msg.data)
        if event['schema'] == 'brython':
            window.location.reload()
        elif event['action']:
            window.jQuery(UI_ELEMENT).trigger(event['schema'], event)
            window.jQuery(UI_ELEMENT).trigger('.'.join([event['schema'], event['action']]), event)

    def _close(evt):
        console.log(evt)

    _WS.bind('open', _open)
    _WS.bind('error', _error)
    _WS.bind('message', _message)
    _WS.bind('close', _close)

def bind(schema=None, action=None, callback=None):
    """ bind event handler """
    assert callable(callback)

    if action:
        routing_key = '.'.join(schema, action)
    else:
        routing_key = schema

    window.jQuery(UI_ELEMENT).on(routing_key, callback)

def trigger(schema=None, action=None, callback=None):
    """ trigger event handler """
    if action:
        routing_key = '.'.join(schema, action)
    else:
        routing_key = schema

    window.jQuery(UI_ELEMENT).trigger(routing_key)

    if callable(callback):
        callback()

def subscribe(schema, oid):
    """ subscribe(schema, oid): lisent for events over WebSocket """
    _WS.send(json.dumps({'bind': [schema, oid]}))

def unsubscribe(schema, oid):
    """ unsubscribe(schema, oid): stop listening for events"""
    _WS.send(json.dumps({'unbind': [schema, oid]}))

def _rpc(method, params=[], callback=None, errback=None):
    """  _rpc(method, params=[], callback=None, errback=None): make JSONRPC POST to backend """
    global _SEQ
    _SEQ = _SEQ + 1
    req = ajax.ajax()

    if callback:
        req.bind('complete', callback)
    else:
        req.bind('complete', echo)

    req.open('POST', _ENDPOINT + '/api', True)
    req.set_header('content-type', 'application/json')
    req.send(json.dumps({'id': _SEQ, 'method': method, 'params': params}))

def _get(resource, callback=None, errback=None):
    """ _get(resource, callback=None, errback=None): make http GET to backend """
    req = ajax.ajax()
    if callback:
        req.bind('complete', callback)
    else:
        req.bind('complete', echo)
    req.open('GET', _ENDPOINT + resource, True)
    req.send()

def echo(req):
    """ echo(req): append return value to terminal as an assignment to a var: '_' """
    doc['code'].value += "\n_ = " + req.response

def schemata(callback=None):
    """ schemata(callback=None): retrieve list of available state machine definitions """
    _get('/schemata', callback=callback)

def state(schema, oid, callback=None):
    """  state(schema, oid, callback=None): get current state """
    _get('/state/%s/%s' % (schema, oid), callback=callback)

def machine(schema, callback=None):
    """ machine(schema, callback=None): get machine definition """
    _get('/machine/%s' % schema, callback=callback)

def dispatch(schema, oid, action, payload={}, callback=None):
    """ dispatch(schema, oid, action, payload={}, callback=None): dispatch new event to endpoint  """
    req = ajax.ajax()

    if callback:
        req.bind('complete', callback)
    else:
        req.bind('complete', echo)

    req.open('POST', _ENDPOINT + '/dispatch/%s/%s/%s' % (schema, oid, action), True)
    req.set_header('content-type', 'application/json')
    req.send(json.dumps(payload))


def stream(schema, oid, callback=None):
    """ stream(schema, oid, callback=None): get all events """
    _get('/stream/%s/%s' % (schema, oid), callback=callback)

def event(schema, eventid, callback=None):
    """ event(schema, eventid, callback=None): get a single event """
    _get('/event/%s/%s' % (schema, eventid), callback=callback)

def exists(schema=None, oid=None, callback=None, errback=None):
    """ exists(schema=None, oid=None, callback=None, errback=None): test for existance of schema and/or stream """

    if not oid:
        _rpc('schema_exists', params=[schema], callback=callback, errback=errback)
    else:
        _rpc('stream_exists', params=[schema, oid], callback=callback, errback=errback)

def load(machine_name, new_schema):
    """ load(machine_name, new_schema): load machine definition as db schema """
    _rpc('schema_create', params=[machine_name, new_schema])

def create(schema, oid):
    """ create(schema, oid): create a new stream """
    _rpc('stream_create', params=[schema, oid])

def destroy(schema):
    """ destroy(schema): drop from db / destroys a schema and all events """
    _rpc('schema_destroy', params=[schema])
