from zope.interface import implements

import os
from twisted.application import service, internet
from twisted.application.service import IServiceMaker, MultiService
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.plugin import IPlugin
from txbitwrap.api import factory as ApiFactory
from txbitwrap.event.dispatch import Dispatcher
from txbitwrap.fswatch import FsWatch
from txbitwrap.session_watch import SessionWatch
from txbitwrap.event import rdq
from txbitwrap import Options
Factory.noisy = False

class ServiceFactory(object):
    implements(IServiceMaker, IPlugin)

    tapname = "bitwrap"
    description = "bitwrap eventstore"
    options = Options

    def makeService(self, options):
        multi_service = MultiService()
        Options.append_env(options)

        bitwrap_node = internet.TCPServer(
            int(options['listen-port']),
            ApiFactory(options),
            interface=options['listen-ip'])

        multi_service.addService(FsWatch(options['brython-path']))
        multi_service.addService(SessionWatch())
        multi_service.addService(bitwrap_node)

        # REVIEW: should this be optional?
        if options['queue']:
            multi_service.addService(Dispatcher(rdq, options))

        return multi_service

serviceMaker = ServiceFactory()
