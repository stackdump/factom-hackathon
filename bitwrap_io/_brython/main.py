""" main app entrypoint """

# TODO: refactor existing brython petri-net editor to work w/ latest brython

import terminal

def application(editor_ns):
    """ load application into editor namespace """ 

    exec("""
    null = None
    true = True
    false = False
    from ctx import Context
    self = Context()
    """, editor_ns)

terminal.onload(callback=application)
