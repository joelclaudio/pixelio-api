from application import app 
import application

from flask import Flask
from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import random
from threading import Thread
from time import sleep
import cyclone.web

active_conections = {}
encoding_hash = {}

def send_data():
    print 'send_data'
    for key, value in active_conections.iteritems():
        value.sendMessage(json.dumps({'cenas': 'altamentes'}, ensure_ascii=True).encode('utf-8'))

class OrionCallbackHandler(cyclone.web.RequestHandler):
    def get(self):
        print 'get'
        return {'cenas': True}
        # for client in clients:
        #     client.sendMessage(payload, isBinary=False)

    def post(self):
        print 'post'
        return {'cenas': True}
        
class ChannelServerProtocol(WebSocketServerProtocol):

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


callback_webapp = cyclone.web.Application([
    (r"/", OrionCallbackHandler),
    (r"/updateCounter", OrionCallbackHandler)
    ])
from autobahn.twisted.websocket import WebSocketServerFactory
websocket_service = WebSocketServerFactory("ws://88.157.229.216:9000")
websocket_service.protocol = ChannelServerProtocol

subscription = LoopingCall(send_data)
subscription.start(1)

reactor.listenTCP(9001, websocket_service)
reactor.listenTCP(5001, callback_webapp, interface="0.0.0.0")

reactor.run()