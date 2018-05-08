"""
"""
import os
from glob import glob
import bitwrap_machine.pnml as petrinet
import bitwrap_machine.dsl as dsl

PNML_PATH = os.environ.get('PNML_PATH', os.path.abspath(__file__ + '/../../schemata'))

def set_pnml_path(pnml_dir):
    global PNML_PATH
    PNML_PATH = pnml_dir

def schema_to_file(name):
    """ build schema filename from name """
    return os.path.join(PNML_PATH, '%s.xml' % name)

def schema_files():
    """ list schema files """
    return glob(PNML_PATH + '/*.xml')

def schema_list():
    """ list schema files """
    return [os.path.basename(xml)[:-4] for xml in schema_files()]

class PTNet(object):
    """ p/t net """

    def __init__(self, name):
        self.name = name
        self.places = None
        self.transitions = None
        self.filename = schema_to_file(name)
        self.net = petrinet.parse_pnml_file(self.filename)[0]

        def reindex():
            """ rebuild net """

            dsl.append_roles(self.net)
            self.places = dsl.places(self.net)
            self.transitions = dsl.transitions(self.net, self.places)
            dsl.apply_edges(self.net, self.places, self.transitions)

        reindex()


    def empty_vector(self):
        """ return an empty state-vector """
        return [0] * len(self.places)

    def initial_vector(self):
        """ return initial state-vector """
        vector = self.empty_vector()

        for _, place in self.places.items():
            vector[place['offset']] = place['initial']

        return vector

    def to_machine(self):
        """ open p/t-net """

        return {
            'state': self.initial_vector(),
            'transitions': self.transitions
        }
