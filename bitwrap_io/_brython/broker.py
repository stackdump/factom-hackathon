from browser import window, console

class Broker(object):

    socket = None

    def __init__(self, config=None):
        console.log('WebsocketBroker enabled')
        Broker.socket = window.io.connect('http://127.0.0.1:8080')
        Broker.socket.on('connect', self.on_connect)

    def on_connect(self):
        console.log('WebsocketBroker connected')
        Broker.socket.emit('message',  { 'hello': 'world' })

