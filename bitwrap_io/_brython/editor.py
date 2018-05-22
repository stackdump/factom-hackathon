import json
from ptnet import PNet
from simulator import Simulation

class EditorBase(object):

    def __init__(self, context=None, config=None):
        self.ctx = context
        self.callback = self.on_select
        self.move_enabled = True

        self.selected_insert_symbol = None
        self.selected_arc_endpoint = None

        self.simulation = None
        self.instance = None
        self.schema = None

    def open(self, name):
        self.schema = name
        self.ctx.machine(self.schema, callback=self.load)

    def load(self, res):
        """ store requested PNML and render as SVG """
        self.instance = PNet(json.loads(res.text), editor=self)
        self.reset(callback=self.render)

    def reset(self, callback=None):
        """ clear SVG and prepare markers """
        if self.instance:
            self.instance.reset()

        if callable(callback):
            callback()

    def render(self, callback=None):
        """ development examples """
        self.instance.render(token_ledger=self.instance.token_ledger)
        self.json_view()

        if callable(callback):
            callback()

    def json_view(self):
        _info = json.dumps({
            'places': self.instance.place_defs,
            'transitions': self.instance.transition_defs,
            'arcs': self.instance.arc_defs,
            'place_names': self.instance.place_names,
            'token_ledger': self.instance.token_ledger
        })

        self.ctx.jQuery('#json').JSONView(_info, {'collapsed': True})

class EditorEvents(EditorBase):
    """ Editor event callbacks """

    def on_click(self, event):
        """ handle mouse events """
        self.callback(event)

    def on_select(self, event):
        """ callback to show attributes for selected element """
        refid, symbol = self._selected(event)

        if not refid:
            return

        # FIXME: should show info in editor
        self.ctx.log('on_select', refid, symbol)

    def on_insert(self, event):
        """ insert a symbol into net """
        if not self.selected_insert_symbol:
            return

        new_coords = [event.offsetX, event.offsetY]
        # TODO: make call to insert new symbol in self.instance

        if self.selected_insert_symbol == 'place':
            self.instance.insert_place(new_coords)
        else:
            self.instance.insert_transition(new_coords)

        self.reset(callback=self.render)

    def on_delete(self, event):
        """ callback when clicking elements when delete tool is active """
        refid, symbol = self._selected(event)

        if not refid:
            return

        if symbol == 'place':
            self.instance.delete_place(refid)
        elif symbol == 'transition':
            self.instance.delete_transition(refid)
        else: # FIXME implement arc handle
            #self.instance.delete_arc(target_id)
            self.ctx.log('delete arc', refid)

        self.reset(callback=self.render)

    def on_trigger(self, event):
        """ callback when triggering a transition during a simulation """
        action = self.simulation.trigger(event)
        self.ctx.log(self.schema, self.simulation.oid, action)
        self.ctx.dispatch(self.schema, self.simulation.oid, action)

    def on_token_inc(self, event):
        return self._token_changed(1, event)

    def on_token_dec(self, event):
        return self._token_changed(-1, event)

    def _token_changed(self, change, event):
        refid, symbol = self._selected(event)

        if not symbol == 'place':
            return

        current = self.instance.token_ledger[refid]
        new_token_count = current + change

        if new_token_count >= 0:
            self.instance.update_place_tokens(refid, new_token_count)
            self.reset(callback=self.render)

    def _selected(self, event):
        target_id = str(event.target.id)

        if not self.is_selectable(target_id):
            return [None, None]

        return target_id.split('-')

    def on_arc_begin(self, event):
        begin = self._selected(event)

        if not begin:
            return 

        self.callback = self.on_arc_end
        self.selected_arc_endpoint = begin

    def on_arc_end(self, event):
        end = self._selected(event)

        if not end:
            return 

        self.callback = self.on_arc_begin
        begin = self.selected_arc_endpoint

        if begin[1] == end[1]:
            return # cannot connect 2 symbols of same type

        if begin[1] == 'transition':
            txn = begin[0]
            place = end[0]
            direction = 'to'
            diff = 1
        else:
            txn = end[0]
            place = begin[0]
            direction = 'from'
            diff = -1

        if txn not in self.instance.arc_defs:
            self.instance.arc_defs[txn] = {'to': [], 'from': []}

        self.instance.arc_defs[txn][direction].append(place)

        offset = self.instance.place_defs[place]['offset']
        self.instance.transition_defs[txn]['delta'][offset] = diff

        self.selected_arc_endpoint = None # reset

        self.reset(callback=self.render)


class Editor(EditorEvents):
    """ Petri-Net editor controls """

    def __init__(self, **kwargs):
        EditorEvents.__init__(self, **kwargs)
        self.bind_controls()

    def bind_controls(self):
        self.ctx.jQuery('#net').on('click', self.on_insert)
        self.ctx.jQuery('.select').on('click', self.select)
        self.ctx.jQuery('.symbol').on('click', self.symbol)
        self.ctx.jQuery('.tool').on('click', self.tool)
        self.ctx.jQuery('.simulator').on('click', self.simulator)

    def select(self, event):
        """ enter select/move mode """
        self.move_enabled = True
        self.selected_insert_symbol = None
        self.callback = self.on_select

    def symbol(self, event):
        """ enter insert symbol mode """
        sym = str(event.target.id)
        self.selected_insert_symbol = sym

    def simulator(self, event):
        """ control start/stop simulation mode """
        target_id = event.target.text

        if target_id == 'reset':
            if self.simulation:
                self.simulation.reset()
            self.callback = self.on_select
            self.move_enabled = True
            self.ctx.clear(txt='>>> ')
        else:
            self.move_enabled = False
            oid = self.ctx.time()
            self.simulation = Simulation(oid, self)
            self.ctx.create(self.schema, oid)
            # FIXME add subscribe after websocket functions
            #self.ctx.subscribe(str(self.schema), str(oid))
            self.ctx.log(self.schema, oid, 'NEW')
            self.callback = self.on_trigger

    def tool(self, event):
        """ modify existing symbol on net """
        self.move_enabled = False
        self.selected_insert_symbol = None
        self.selected_arc_endpoint = None
        target_id = str(event.target.id)

        if target_id == 'arc':
            self.callback = self.on_arc_begin
        elif target_id == 'delete':
            self.callback = self.on_delete
        elif target_id == 'dec_token':
            self.callback = self.on_token_dec
        elif target_id == 'inc_token':
            self.callback = self.on_token_inc

    def is_selectable(self, target_id):
        """ determine if element allows user interaction """

        # KLUDGE: relies on a naming convention
        # 'primary' labels for symbols are assumed not to use the char '-'
        # 'secondary' labels use IDs with the form <primary>-<secondary>

        if '-' not in target_id:
            return False
        else:
            return True
