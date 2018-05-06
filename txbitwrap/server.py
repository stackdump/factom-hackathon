import os
import uuid
import sys

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from flask import Flask, render_template

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource


class EchoServerProtocol(WebSocketServerProtocol):
    """ Testing websocket echo """

    def onMessage(self, payload, isBinary):
        """ just return payload """
        self.sendMessage(payload, isBinary)

app = Flask( __name__, template_folder=os.path.abspath(os.path.dirname(__file__) + '/../txbitwrap/templates'))

@app.route('/')
def page_home():
    return render_template('index.html')

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
