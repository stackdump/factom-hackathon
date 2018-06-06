"""
dsl - methods for constructing a bitwrap schema

Uses Petri-Net Markup as a "Domain Specific Language" (DSL) to define a bitwrap machine.

"""

from bitwrap_io.machine.pnml import Transition, Place

def places(net):
    """ build place vector definition """

    _places = {}
    offset = 0

    for place in net.places:

        _places[place] = {
            'offset': offset,
            'position': net.places[place].position,
            'initial': net.places[place].marking
        }

        offset += 1

    return _places

def empty_vector(size):
    """ return an empty vector of given size """
    return [0] * size

def transitions(net, net_places):
    """ build set of transitions from network """

    _transitions = {}

    for action in net.transitions:
        _transitions[action] = {
            'delta': empty_vector(len(net_places)),
            'position': net.transitions[action].position
        }

    return _transitions

def apply_edges(net, net_places, net_transitions):
    """ re-index edges and places """

    for edge in net.edges:
        source = edge.find_source()
        target = edge.find_target()

        if isinstance(source, Transition):
            if edge.inhibitor is True:
                raise Exception('Roles cannot be targets')
            else:
                offset = net_places[target.id]['offset']
                net_transitions[source.id]['delta'][offset] = 1

        elif isinstance(source, Place):
            if not edge.inhibitor:
                offset = net_places[source.id]['offset']
                net_transitions[target.id]['delta'][offset] = -1
        else:
            raise Exception('invalid edge %s' % edge.id)
