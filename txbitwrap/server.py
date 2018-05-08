import os
import uuid
import sys

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import request, g, session, flash, redirect, url_for, render_template, send_from_directory
from flask_github import GitHub

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource

from bitwrap_io.api import application as app

class EchoServerProtocol(WebSocketServerProtocol):
    """ Testing websocket echo """

    def onMessage(self, payload, isBinary):
        """ just return payload """
        self.sendMessage(payload, isBinary)

app.template_folder = os.path.abspath(os.path.dirname(__file__) + '/../txbitwrap/templates')
app.static_url_path = ''
app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')
app.config['DEBUG'] = True

github = GitHub(app)

@app.route('/<path:path>')
def send_brython(path):
    return send_from_directory('../bitwrap_brython', path)

@app.route('/')
def index():
    return render_template('index.html')

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

    #log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    wsFactory = WebSocketServerFactory(u"ws://127.0.0.1:8080") # TODO get from options
    wsFactory.protocol = EchoServerProtocol
    wsResource = WebSocketResource(wsFactory)

    # create a Twisted Web WSGI resource for our Flask server
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    # create a Twisted Web Site and run everything
    return Site(rootResource)
