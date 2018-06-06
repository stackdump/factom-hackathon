import json

class Controller(object):
    """ control loading and saving network definitions """

    def __init__(self, context=None, editor=None, default_net='counter'):
        self.editor = editor
        self.ctx = context
        self.select_net = default_net
        self.view(select_net=default_net)
        self.ctx.schemata(callback=self.load_saved_nets)
        self.bind_controls()

    def bind_controls(self):
        """ control editor instance """
        self.ctx.jQuery('#netreload').on('click', lambda _: self.view())
        self.ctx.jQuery('#netsave').on('click', lambda _: self.save())

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

    def save(self):
        """ upload petrinet xml """
        def _log(req):
            self.ctx.log(req.text)

        def _upload():
            xml = self.editor.export()
            self.ctx.upload_pnml(self.selected_net, xml, callback=_log, errback=_log)

        self.editor.save(callback=_upload)

    def view(self, select_net=None):
        """ open net with editor """
        if select_net:
            self.selected_net = select_net

        self.editor.open(self.selected_net)
