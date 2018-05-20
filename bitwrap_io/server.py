# -*- coding: utf-8 -*-
import os
import uuid

from flask import request, g, session, flash, redirect, url_for, render_template, send_from_directory

from bitwrap_io.api import app, socketio, github

BRYTHON_FOLDER = os.path.abspath(os.path.dirname(__file__) + '/_brython')

@socketio.on('message')
def handle_message(message):
    print('received message: ', message)

@app.route('/<path:path>')
def send_brython(path):
    """ serve static brython files """
    return send_from_directory(BRYTHON_FOLDER, path)

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

    # create a Twisted Web WSGI resource
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    return Site(rootResource)

if __name__ == '__main__':
    #app.debug = True
    #socketio.run(app, use_reloader=True, log_output=True, port=8080)

    from livereload import Server
    server = Server(app.wsgi_app)
    server.watch('./bitwrap_io/_brython/')
    server.serve(port=8080)
