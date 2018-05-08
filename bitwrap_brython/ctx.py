""" ctx: Bitwrap 'context' - see command list: ctx.commands - see docstring: help(ctx.<command>) """

import dsl
import json
from browser import window, document
from dsl import bind, trigger, subscribe, unsubscribe, echo # util
from dsl import load, create, destroy # modify stream
from dsl import schemata, state, machine, dispatch, stream, event, exists # use stream

commands = [
    'bind',
    'trigger',
    'subscribe',
    'unsubscribe',
    'load',
    'create',
    'destroy',
    'schemata',
    'state',
    'machine',
    'dispatch',
    'stream',
    'event',
    'exists'
]

from dsl import subscribe, unsubscribe, echo # util
from dsl import load, create, destroy # modify stream
from dsl import schemata, state, machine, dispatch, stream, event, exists # use stream
import ctl
from ctl import on_event

def __onload(version=None, callback=None):
    """ init config and connections """

    def application(req):
        """ load application """ 
        config = json.loads(req.response)
        dsl.__onload(config)
        ctl.__onload(dsl)

        document['code'].value = "txbitwrap on %s %s\n>>> " % ( window.navigator.appName, window.navigator.appVersion)
        document['code'].value += "help(ctx)"
        document['code'].focus()

        if callable(callback):
            callback(config)

    dsl._get(window.Bitwrap.config, application)
