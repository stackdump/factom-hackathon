import json

class Controller(object):
    """ control loading and saving network definitions """

    def __init__(self, context=None, editor=None):
        self.editor = editor
        self.ctx = context
        self.ctx.schemata(callback=self.load_saved_nets)
        self.view('octoe')

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

    def view(self, name):
        self.selected_net = name
        self.editor.open(self.selected_net)
