# -*- coding: utf-8 -*-
import os
import uuid

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from flask import request, g, session, flash, redirect, url_for, render_template, send_from_directory
from flask_github import GitHub

from bitwrap_io.api import app

BRYTHON_FOLDER = os.path.abspath(os.path.dirname(__file__) + '/_brython')

class EchoServerProtocol(WebSocketServerProtocol):
    """ Testing websocket echo """

    def onMessage(self, payload, isBinary):
        """ just return payload """
        self.sendMessage(payload, isBinary)

app.template_folder = os.path.abspath(os.path.dirname(__file__) + '/../templates')
app.static_url_path = ''
app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')

github = GitHub(app)

@app.route('/<path:path>')
def send_brython(path):
    """ serve static brython files """
    return send_from_directory(BRYTHON_FOLDER, path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    #user = User.query.filter_by(github_access_token=oauth_token).first()
    #if user is None:
    #    user = User(oauth_token)
        #db_session.add(user)

    #user.github_access_token = oauth_token
    #db_session.commit()
    return redirect(next_url)

def factory(options):
    # TODO: update to accept args from options
    app.secret_key = str(uuid.uuid4())

    # TODO get from options for ip
    wsFactory = WebSocketServerFactory(u"ws://127.0.0.1:8080")
    wsFactory.protocol = EchoServerProtocol
    wsResource = WebSocketResource(wsFactory)

    # create a Twisted Web WSGI resource
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    return Site(rootResource)

if __name__ == '__main__':
    from livereload import Server
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch('./bitwrap_io/_brython/')
    server.serve(port=8080)
