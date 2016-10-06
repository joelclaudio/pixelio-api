from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import random
from threading import Thread
import time 
import json
import thread

active_conections = {}
encoding_hash = {}

def send_data():
    print 'send_data'
    for key, value in active_conections.iteritems():
        value.sendMessage(json.dumps({'cenas': 'altamentes'}, ensure_ascii=True).encode('utf-8'))


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        active_conections.update({
            request.params['id'][0]: self
        })
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        del active_conections[self.http_request_params['id'][0]]
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor
    from twisted.internet.task import LoopingCall

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://88.157.229.216:9000")
    factory.protocol = MyServerProtocol

    subscription = LoopingCall(send_data)
    subscription.start(1) 

    reactor.listenTCP(9000, factory)
    reactor.run()

