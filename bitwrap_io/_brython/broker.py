from browser import window, console

class Broker(object):

    socket = None

    def __init__(self, config=None):
        Broker.socket = window.io.connect('http://127.0.0.1:8080')
        Broker.socket.on('commit', self.on_commit)

    def on_commit(self, msg):
        console.log(msg)
