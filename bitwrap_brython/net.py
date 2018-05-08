from browser import window, document, console
import json

PAPER = None
"""
Snap.svg instance
"""

NETS = {}
"""
petr-net definitions
"""

SYMBOLS = {}
"""
svg graphic elements used to render a Petri-Net
"""

SCHEMA = None
"""
petri-net in use
"""

INSTANCE = None
"""
elements and network state
"""

CTL = None
"""
reference to controller
"""

def on_load():
    """ use snap to generate the symbols needed to render a petri-net """
    window.SYMBOLS = SYMBOLS
    SYMBOLS['arrow'] = Draw._arrow()
    Draw.origin()

def _attr(sym):
    """ access attributes of an existing symbol """
    return SYMBOLS[sym].node.attributes

class Draw(object):
    """ Use Snap.SVG to draw PNet graph """

    @staticmethod
    def origin(x1=0, y1=0, x2=100, y2=100):
        """ draw x/y axis """

        PAPER.line({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': 0,
        }).attr({
            'id': 'origin_x',
            'class': 'origin',
            'stroke': '#000',
            'strokeWidth': 2,
            'markerEnd': SYMBOLS['arrow']
        })

        PAPER.line({
            'x1': x1,
            'y1': y1,
            'x2': 0,
            'y2': y2,
        }).attr({
            'id': 'origin_y',
            'class': 'origin',
            'stroke': '#000',
            'strokeWidth': 2,
            'markerEnd': SYMBOLS['arrow']
        })

    @staticmethod
    def handle(x=0, y=50, size=40, refid=None, symbol=None):
        """
        add group of elements needed for UI interaction
        here mouse events are bound to controler actions
        """
        _id = refid + '-handle'

        point = SYMBOLS[refid]
        handle = PAPER.g(point, Draw._label(refid))

        if symbol == 'place':
           el = Draw._place(x=x, y=y, size=size, refid=refid, symbol=symbol)
           el.data('refid', refid)
           token_el = Draw._tokens(refid)
           handle.add(el, token_el)

        elif symbol == 'transition':
           el = Draw._transition(x=x, y=y, size=size, refid=refid, symbol=symbol)
           handle.add(el)

        el.data('refid', refid)
        SYMBOLS[_id] = handle

        def _drag_start(x, y, evt):
            """ begin mouse interaction """
            CTL.on_click(evt)

        def _drag_end(evt):
            """ complete mouse interaction """
            if not CTL.move_enabled:
                return

            def _move_and_redraw():
                """ trigger action in UI """

                try:
                    delta = handle.data('tx')

                    if symbol == 'place':
                        _defs = INSTANCE.place_defs
                    elif symbol == 'transition':
                        _defs = INSTANCE.transition_defs

                    _coords = _defs[refid]['position']
                    _defs[refid]['position'] = [int(_coords[0] + delta[0]), int(_coords[1] + delta[1])]
                except:
                    pass # skip if delta is not set
                finally:
                    CTL.render()

            CTL.reset(callback=_move_and_redraw)

        def _dragging(dx, dy, x, y, event):
            """ svg transformation while dragging """
            if not CTL.move_enabled:
                return

            _tx = 't %i %i' % (dx, dy)
            handle.transform(_tx)
            handle.data('tx', [dx, dy])
        
        handle.drag(_dragging, _drag_start, _drag_end)

        return el

    @staticmethod
    def place(x, y, label=None):
        """ adds a place node """
        return Draw._node(x, y, label=label, symbol='place')

    @staticmethod
    def transition(x, y, label=None):
        """ adds a transition node """
        return Draw._node(x, y, label=label, symbol='transition')

    @staticmethod
    def arc(sym1, sym2, token_weight=1):
        """ draw arc between 2 points """
        x1 = float(_attr(sym1).x2.value)
        y1 = float(_attr(sym1).y2.value)
        x2 = float(_attr(sym2).x2.value)
        y2 = float(_attr(sym2).y2.value)

        if SYMBOLS[sym2].data('symbol') == 'place':
            start='transition'
            end='place'
        else:
            end='transition'
            start='place'

        _id = '%s-%s' % (sym1, sym2)
        el = Draw._arc(x1, y1, x2, y2, refid=_id, start=start, end=end)
        el.data('symbol', 'arc')
        el.data('start', sym1)
        el.data('end', sym2)

        return el

    @staticmethod
    def _node(x, y, label=None, symbol=None):
        """ adds a petri-net symbol to the graph """

        point_el= Draw._point(x=x, y=y, refid=label)
        point_el.data('symbol', symbol)
        point_el.data('label', label)

        SYMBOLS[label] = point_el
        return point_el

    @staticmethod
    def _point(x=0, y=0, refid=None):
        """ draw hidden point """

        el = PAPER.line({
            'x1': 0,
            'y1': 0,
            'x2': x,
            'y2': y,
        }).attr({
            'id': refid,
            'class': 'point',
            #'stroke': '#87CDDE',
            'strokeWidth': 2
        })

        SYMBOLS[refid] = el
        return el


    @staticmethod
    def _arc(x1, y1, x2, y2, weight=1, refid=None, start=None, end=None):
        """
        draw arc with arrow
        This also adjusts x coordintates to match place/transition size
        """

        if start == 'place':
            if x1 > x2:
                x1 = x1 - 20 
                x2 = x2 + 10
            else:
                x1 = x1 + 20
                x2 = x2 - 10
        elif end == 'place':
            if x1 > x2:
                x1 = x1 - 5 
                x2 = x2 + 20
            else:
                x1 = x1 + 5
                x2 = x2 - 20
        
        el = PAPER.line({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        }).attr({
            'id': refid,
            'class': 'arc',
            'stroke': '#000',
            'stroke-opacity': '0.8',
            'strokeWidth': 1,
            'markerEnd': SYMBOLS['arrow']
        })

        SYMBOLS[refid] = el
        return el

    @staticmethod
    def _arrow():
        """ arrowhead """

        return PAPER.path(
            "M 2 59 L 293 148 L 1 243 L 121 151 Z"
        ).marker({
            'x': 0,
            'y': 0,
            'width': 8000,
            'height': 8000,
            'refX': 260,
            'refY': 150
        }).attr({
            'fill':'white',
            'stroke': 'black',
            'strokeWidth': 10,
            'markerUnits':'strokeWidth',
            'markerWidth': 350,
            'markerHeight':350,
            'orient': "auto" 
        })

    @staticmethod
    def _tokens(sym):
        """ token values """

        _id = refid + '-tokens'

        value = int(INSTANCE.token_ledger[sym])

        # TODO: draw numbers <= 5 as dots
        if value == 1:

            return PAPER.circle({
                'cx': float(_attr(sym).x2.value),
                'cy': float(_attr(sym).y2.value),
                'r': 2
            }).attr({
                'id': _id,
                'class': 'tokens',
                'fill': '#000',
                'fill-opacity': 1,
                'stroke': '#000',
                'orient': 0 
            })

        if value == 0:
            _txt = ''
        else:
            _txt = str(value)

        return PAPER.text(
            float(_attr(sym).x2.value),
            float(_attr(sym).y2.value),
            _txt
        ).attr({
            'id': refid + '-txtlabel',
            'class': 'txtlabel'
        })

    @staticmethod
    def _label(sym):
        """ add txt label to a symbol """

        _id = refid + '-label'

        _txt = SYMBOLS[sym].data('label')

        el = PAPER.text(float(_attr(sym).x2.value) - 10, float(_attr(sym).y2.value) + 35, _txt)
        el.attr({ 'class': 'label', 'style': 'font-size: 12px;'})
        return el

    @staticmethod
    def _transition(x=0, y=50, size=40, refid=None, symbol=None):
        """ draw transition """

        _id = '%s-%s' % (refid, symbol)

        return PAPER.rect({
            'x': x - 5,
            'y': y - 17,
            'width': 10,
            'height': 34,
        }).attr({
            'id': _id,
            'class': symbol,
            'fill': 'black',
            'fill-opacity': 1,
            'stroke': '#000',
            'strokeWidth': 2,
            'orient': 0 
        })

    @staticmethod
    def _place(x=0, y=50, size=40, refid=None, symbol=None):
        """ draw place """

        _id = '%s-%s' % (refid, symbol)

        return PAPER.circle({
            'cx': x,
            'cy': y,
            'r': (size/2)
        }).attr({
            'id': _id,
            'class': symbol,
            'fill': '#FFF',
            'fill-opacity': 1,
            'stroke': '#000',
            'orient': 0 
        })


class RenderMixin(object):
    """ interface for rendering PNet as an SVG """

    def render(self):
        """ draw the petri-net """
        self.draw_nodes()
        self.draw_handles()
        self.draw_arcs()


    def draw_nodes(self):
        """ draw points used to align other elements """

        for name, attr in self.place_defs.items():
            el = Draw.place(attr['position'][0], attr['position'][1], label=name)
            el.data('offset', attr['offset'])
            el.data('initial', attr['initial']) 

            self.places[name] = el

        for name, attr in self.transition_defs.items():
            el = Draw.transition(attr['position'][0], attr['position'][1], label=name)
            self.transitions[name] = el

    def draw_handles(self):
        """ draw places and transitions """

        for label, pl in self.places.items():
            self.handles[label] = Draw.handle(
                x=float(pl.node.attributes.x2.value),
                y=float(pl.node.attributes.y2.value),
                refid=label,
                symbol='place'
            )

        for label, tx in self.transitions.items():
            self.handles[label] = Draw.handle(
                x=float(tx.node.attributes.x2.value),
                y=float(tx.node.attributes.y2.value),
                refid=label,
                symbol='transition'
            )

    def draw_arcs(self):
        """ draw the petri-net """

        for txn, attrs in self.arc_defs.items():

            if attrs['to']:
                for label in attrs['to']:
                    el = Draw.arc(txn, label)
                    self.arcs.append(el)

            if attrs['from']:
                for label in attrs['from']:
                    el = Draw.arc(label, txn)
                    self.arcs.append(el)

class PNet(RenderMixin):

    def __init__(self, control):
        """ persistent Petri-Net object """

        global INSTANCE
        INSTANCE = self

        global CTL
        CTL = control

        self.places = {}
        self.place_names = {}
        self.place_defs = {}

        self.vector_size = 0
        self.token_ledger = {}

        self.arcs = []
        self.arc_defs = {}

        self.transition_defs = {}
        self.transitions = {}

        self.handles = {}
        self.reindex()

    def reindex(self):
        """ rebuild data points """

        for name, attr in NETS[SCHEMA]['places'].items():
            self.place_names[attr['offset']] = name
            self.place_defs[name] = attr

            if name not in self.token_ledger:
                self.token_ledger[name] = attr['initial']

        self.vector_size = len(self.place_defs)

        for name, attr in NETS[SCHEMA]['transitions'].items():
            if name not in self.arc_defs:
                self.arc_defs[name] = { 'to': [], 'from': [] }

            for i in range(0, self.vector_size):
                if attr['delta'][i] > 0:
                    self.arc_defs[name]['to'].append(self.place_names[i])

                elif attr['delta'][i] < 0:
                    self.arc_defs[name]['from'].append(self.place_names[i])

            self.transition_defs[name] = attr

    def reset_tokens(self):
        """ rebuild token counters to initial state """
        # FIXME somehow get leftovers when removing all elements
        #self.token_ledger = {}

        for name, attr in NETS[SCHEMA]['places'].items():
            self.token_ledger[name] = attr['initial']

    def _new_place_name(self):
        for i in range(0, self.vector_size):
            label = 'p%i' % i

            if label not in self.place_defs:
                return label

        return None

    def insert_place(self, coords, initial=0):
        """ add place symbol to net """
        _offset = self.vector_size
        self.vector_size = _offset + 1

        label = self._new_place_name()
        assert label

        self.place_defs[label] = {
            'position': coords,
            'initial': initial,
            'offset': _offset
        }

        self.place_names[_offset] = label
        self.token_ledger[label] = initial

        for name, attr in self.transition_defs.items():
            attr['delta'].append(0)

    def _new_transition_name(self):
        for i in range(0, len(self.transition_defs) + 1):
            label = 't%i' % i

            if label not in self.transition_defs:
                return label

        return None

    def insert_transition(self, coords):
        """ add transition symbol to net """
        label = self._new_transition_name()

        self.transition_defs[label] = {
            'position': coords,
            'role': 'default',
            'delta': [0] * self.vector_size
        }

    def update(self, statevector):
        """
        update token counters by
        setting a new statevector
        """

        for name, attr in self.place_defs.items():
            self.token_ledger[name] = statevector[attr['offset']]

    def update_place_tokens(self, name, token_count):
        """
        update token counters for specific place
        """

        self.token_ledger[name] = token_count

    def delete_place(self, refid):
        """ remove a place symbol from net """

        # FIXME this seems to leave stom place names


        #console.log(self.place_defs[refid])
        offset = self.place_defs[refid]['offset']

        for idx, name in self.place_names.items():
            if name == refid:
                del self.place_names[idx]
                break

        for label in self.transition_defs.keys():
            del self.transition_defs[label]['delta'][offset]

        self.vector_size = len(self.place_defs)
        self.delete_arcs_for_symbol(refid)

        for _, attr in self.place_defs.items():
            if attr['offset'] > offset:
                attr['offset'] = attr['offset'] - 1

        del self.token_ledger[refid]
        del self.place_defs[refid]
        del self.places[refid]

    def delete_transition(self, refid):
        """ remove a transition symbol from net """
        try:
            del self.transition_defs[refid]
            del self.arc_defs[refid]
            del self.transitions[refid]
        except:
            pass

    def delete_arcs_for_symbol(self, refid):
        """ remove arcs associated with a given place or transition """

        # FIXME doesn't remove arc consistently
        for label, attrs in self.arc_defs.items():
            if refid in attrs['to']:
                self.arc_defs[label]['to'].remove(refid)

            if refid in attrs['from']:
                self.arc_defs[label]['from'].remove(refid)

