# -*- coding: utf-8 -*-
"""
Provide resources for bitwrap HTTP API
"""
import os
import json

import socketio

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_github import GitHub

import bitwrap_io.machine as pnml
from bitwrap_io.machine import ptnet
from bitwrap_io.rpc import eventstore, call

app = Flask(__name__)

app.template_folder = os.path.abspath(os.path.dirname(__file__) + '/../templates')
app.static_url_path = ''
app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')

CORS(app)
api = Api(app)
sio = socketio.Server(async_mode='eventlet', cookie='bitwrap')
github = GitHub(app)

VERSION = 'v0.3.0'

def commit(schema, oid, action, payload):
    """ append event to eventstore """

    res = eventstore(schema)(oid=oid, action=action, payload=payload)
    res['action'] = action
    sio.emit('commit', res)
    return res

@sio.on('dispatch')
def dispatch(sid, evt):
    """ handle event commit over socketio """
    commit(evt['schema'], evt['oid'], evt['action'], evt['payload'])

class Rpc(Resource):
    """ handle rpc call """
    # TODO: enforce permissions

    def post(self):
        """
        handle rpc calls

        will accept post body
        or
        form encoded request with a field called 'json'
        """
        res = {}
        req = {}

        try:
            if request.data == '':
              payload = request.form.get('json')
            else:
              payload = request.data

            if type(payload) is bytes:
                payload = payload.decode('utf8')

            req = json.loads(payload)
            res['id'] = req.get('id')
            res['result'] = call(req['method'], req['params'])
            res['error'] = None
        except Exception as ex:
            msg = str(ex).splitlines()[0]
            res = {'id': req.get('id'), 'error': msg}

        return res, 200, None


class Dispatch(Resource):
    """ dispatch event over REST api """

    def post(self, schema, oid, action):
        if not request.data:
            event = request.form.get('json')
        else:
            event = request.data

        if not event:
            event = '{}'

        if type(event) is bytes:
            payload = event.decode('utf8')
        else:
            payload = event

        res = commit(schema, oid, action, payload)

        return res, 200, None

class Event(Resource):
    """ fetch specific event by eventid """

    def get(self, schema, eventid):
        res = eventstore(schema).storage.db.events.fetch(eventid)
        return res, 200, None

class Machine(Resource):
    """ get state machine defs """

    def get(self, schema):
        machine = pnml.Machine(schema)
        res = {
            'machine': {
                'name': schema,
                'places': machine.net.places,
                'transitions': machine.net.transitions
            }
        }

        return res, 200, None

class Schemata(Resource):
    """ get list of state machine schemata """

    def get(self):
        res = {'schemata': ptnet.schema_list()}
        return res, 200, None

class State(Resource):
    """ get state of a given stream """

    def get(self, schema, oid):
        res = eventstore(schema).storage.db.states.fetch(oid)
        return res, 200, None

class Stream(Resource):
    """ retrieve a stream of events by stream oid """

    def get(self, schema, stream_oid):
        res = eventstore(schema).storage.db.events.fetchall(stream_oid)
        return res, 200, None

class Config(Resource):
    """ config browser app """

    use_websocket = True
    """ flag used by front-end to decide whether to use websocket """

    def get(self, stage):
        """ direct web app to api """

        res = {
            'endpoint': os.environ.get('ENDPOINT', ''),
            'version': VERSION,
            'stage': stage,
            'use_websocket': self.use_websocket
        }
        return res, 200, None

def __load_routes():
    """ load resource routes """

    routes = [
        dict(resource=Dispatch, urls=['/dispatch/<schema>/<oid>/<action>'], endpoint='dispatch'),
        dict(resource=State, urls=['/state/<schema>/<oid>'], endpoint='state'),
        dict(resource=Machine, urls=['/machine/<schema>'], endpoint='machine'),
        dict(resource=Event, urls=['/event/<schema>/<eventid>'], endpoint='event'),
        dict(resource=Stream, urls=['/stream/<schema>/<streamid>'], endpoint='stream'),
        dict(resource=Schemata, urls=['/schemata'], endpoint='schemata'),
        dict(resource=Rpc, urls=['/api'], endpoint='api'),
        dict(resource=Config, urls=['/config/<stage>.json'], endpoint='config')
    ]

    for route in routes:
        api.add_resource(route.pop('resource'), *route.pop('urls'), **route)

__load_routes()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
