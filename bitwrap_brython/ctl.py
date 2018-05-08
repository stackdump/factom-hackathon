from browser import window, document as doc, console
import net
import sim
import json

CTX = None
"""
Bitwrap context
"""

CTL = None
"""
UI control interface
"""

def __onload(ctx):
    """ use snap to begin creating an SVG """
    global CTL
    CTL = Editor()

    window.jQuery('#net').on('click', CTL.on_insert)
    window.jQuery('.select').on('click', CTL.select)
    window.jQuery('.symbol').on('click', CTL.symbol)
    window.jQuery('.tool').on('click', CTL.tool)
    window.jQuery('.simulator').on('click', CTL.simulator)

    global CTX
    CTX = ctx

    # TODO: control from UI
    # maybe add a dropdown
    #CTX.machine('counter', callback=CTL.load)
    CTX.machine('octoe', callback=CTL.load)

def on_event(_, event):
    """ receive event over jQuery binding"""
    if 'action' in event:
        return CTL.simulation.execute(event['action'])

class Controller(object):
    """ Provide interface for UI actions """

    def load(self, res):
        """ store requested PNML and render as SVG """
        pnet = json.loads(res.text)
        net.SCHEMA = pnet['machine']['name']
        net.NETS[net.SCHEMA] = pnet['machine']
        self.reset(callback=self.render)

    def reset(self, callback=None):
        """ clear SVG and prepare markers """
        net.PAPER
        
        if not net.PAPER:
            net.PAPER=window.Snap('#net')

        net.PAPER.clear()
        net.on_load()

        if callable(callback):
            callback()

    def render(self, callback=None):
        """ development examples """
        if not net.INSTANCE:
            net.PNet(self)

        net.INSTANCE.render()
        self.json_view()

        if callable(callback):
            callback()

    def json_view(self):
        _info = json.dumps({
            'places': net.INSTANCE.place_defs,
            'transitions': net.INSTANCE.transition_defs,
            'arcs': net.INSTANCE.arc_defs,
            'place_names': net.INSTANCE.place_names,
            'token_ledger': net.INSTANCE.token_ledger
        })

        window.jQuery('#json').JSONView(_info)

class EditorEvents(object):
    """ Editor event callbacks """

    def on_click(self, event):
        """ handle mouse events """
        self.callback(event)

    def on_select(self, event):
        """ callback to show attributes for selected element """
        refid, symbol = self._selected(event)

        if not refid:
            return

        console.log('on_select', refid, symbol)
        # FIXME: should show info in editor

    def on_insert(self, event):
        """ insert a symbol into net """
        if not self.selected_insert_symbol:
            return

        new_coords = [event.offsetX, event.offsetY]
        # TODO: make call to insert new symbol in INSTANCE

        if self.selected_insert_symbol == 'place':
            net.INSTANCE.insert_place(new_coords)
        else:
            net.INSTANCE.insert_transition(new_coords)

        self.reset(callback=self.render)

    def on_delete(self, event):
        """ callback when clicking elements when delete tool is active """
        refid, symbol = self._selected(event)

        if not refid:
            return

        if symbol == 'place':
            net.INSTANCE.delete_place(refid)
        elif symbol == 'transition':
            net.INSTANCE.delete_transition(refid)
        else: # FIXME implement arc handle
            #net.INSTANCE.delete_arc(target_id)
            console.log('delete arc', refid)

        self.reset(callback=self.render)

    def on_trigger(self, event):
        """ callback when triggering a transition during a simulation """
        action = CTL.simulation.trigger(event)
        console.log(net.SCHEMA, CTL.simulation.oid, action)
        CTX.dispatch(net.SCHEMA, self.simulation.oid, action)

    def on_token_inc(self, event):
        return self._token_changed(1, event)

    def on_token_dec(self, event):
        return self._token_changed(-1, event)

    def _token_changed(self, change, event):
        refid, symbol = self._selected(event)

        if not symbol == 'place':
            return

        current = net.INSTANCE.token_ledger[refid]
        new_token_count = current + change

        if new_token_count >= 0:
            net.INSTANCE.update_place_tokens(refid, new_token_count)
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

        if txn not in net.INSTANCE.arc_defs:
            net.INSTANCE.arc_defs[txn] = {'to': [], 'from': []}

        net.INSTANCE.arc_defs[txn][direction].append(place)

        offset = net.INSTANCE.place_defs[place]['offset']
        net.INSTANCE.transition_defs[txn]['delta'][offset] = diff

        self.selected_arc_endpoint = None # reset

        self.reset(callback=self.render)

class Editor(Controller, EditorEvents):
    """ Petri-Net editor controls """

    def __init__(self):
        self.callback = self.on_select
        self.move_enabled = True
        self.selected_insert_symbol = None
        self.selected_arc_endpoint = None
        self.simulation = None

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
            doc['code'].value = '>>>'
        else:
            self.move_enabled = False
            oid = window.Date.now()
            self.simulation = sim.Simulation(oid, net.INSTANCE, self)
            CTX.create(net.SCHEMA, oid)
            CTX.subscribe(str(net.SCHEMA), str(oid))
            console.log(net.SCHEMA, oid, 'NEW')
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
