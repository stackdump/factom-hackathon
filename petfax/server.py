#!/usr/bin/env python

from livereload import Server

import bitwrap_io.server
from bitwrap_io.api import Config
from bitwrap_io.server import app, pnml_editor

from flask_restful import Resource, Api

class VetChain(Resource):
    """ save new Petri-Net XML definition """

    def post(self, vetid):
        machine_def = request.data

        if type(machine_def) is bytes:
            payload = machine_def.decode('utf8')
        else:
            payload = machine_def

        print(payload)

        # TODO: create vet chain
        return {'saved': True, 'schema': schema}, 200, None


# run livereload for brython development
if __name__ == '__main__':
    api = pnml_editor(app)

    routes = [
        dict(resource=VetChain, urls=['/vetchain/<vetid>'], endpoint='vetchain'),
    ]

    for route in routes:
        api.add_resource(route.pop('resource'), *route.pop('urls'), **route)

    # livereload is not compatible with socketio
    # so disable websocket usage
    Config.use_websocket = False

    server = Server(app.wsgi_app)
    server.watch('./bitwrap_io/_brython/')
    server.serve(port=8080)
