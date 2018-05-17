import json

class Controller(object):
    """ control loading and saving network definitions """

    def __init__(self, context=None, editor=None):
        self.editor = editor
        self.ctx = context
        self.select_net = 'untitled'
        self.onload()

    def onload(self):
        self.view(select_net='counter')
        self.ctx.schemata(callback=self.load_saved_nets)
        self.bind_controls()

    def load_saved_nets(self, req):
        """ load known schemata from server """
        nets = json.loads(req.text)['schemata']
        options = []

        for net in nets:
            if self.selected_net == net:
                options.append('<option selected="selected">%s</option>' % net)
            else:
                options.append('<option>%s</option>' % net)

        el = self.ctx.jQuery('#netselect')
        el.html(''.join(options))
        el.change(lambda event: self.view(event.target.value))

    def bind_controls(self):
        """ control editor instance """
        self.ctx.jQuery('#netreload').on('click', lambda _: self.view())

    def view(self, select_net=None):
        if select_net:
            self.selected_net = select_net

        self.editor.open(self.selected_net)
