from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

from bitwrap_io.server import factory

class Options(usage.Options):
    # TODO: add other bitwrap options
    optParameters = [["port", "p", 8080, "The port number to listen on."]]


@implementer(IServiceMaker, IPlugin)
class BitwrapServiceMaker(object):
    tapname = "bitwrap"
    description = "bitwrap eventstore api"
    options = Options

    def makeService(self, options):
        """ Construct a TCPServer """
        return internet.TCPServer(int(options["port"]), factory(options))

serviceMaker = BitwrapServiceMaker()
