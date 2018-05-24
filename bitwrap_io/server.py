# -*- coding: utf-8 -*-
import os
import eventlet
import eventlet.wsgi
import uuid

from flask import request, g, session, flash, redirect, url_for, render_template, send_from_directory

import socketio

from bitwrap_io.api import app, sio, github

BRYTHON_FOLDER = os.path.abspath(os.path.dirname(__file__) + '/_brython')

@sio.on('message')
def handle_message(sid, data):
    print('received message: ', data)

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

if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    sioapp = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 8080)), sioapp)
