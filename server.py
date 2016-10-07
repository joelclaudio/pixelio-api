import application

from application.utils import cisco

from application.logic import GameWorld

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
from flask import Response
from application import app_logic

import json

active_conections = {}
encoding_hash = {}

def send_data():
    for key, value in active_conections.iteritems():
        value.sendMessage(json.dumps({'cenas': 'altamentes'}, ensure_ascii=True).encode('utf-8'))

def fetch_info():
    app_logic.fetch_all_clients()
    for key, value in active_conections.iteritems():
        value.sendMessage(json.dumps(app_logic.get_game_info(key), ensure_ascii=True).encode('utf-8'))

class ProfileHandler(cyclone.web.RequestHandler):
    def get(self):
        mac_address =  self.request.uri.split('?macAddress=')
        if len(mac_address) > 0:
            mac_address = mac_address[len(mac_address)-1]


        success, message, data, created = logic.get_profile_by_mac_address(mac_address)
        print success, message, data, created
        return success, message, data, created

    def post(self):
        headers = self.request.headers
        if 'MacAddress' not in headers:
            return response_models.response_failed(message="mac_address_not_found")

        mac_address =  headers.get('MacAddress')
        success, message, data = app_logic.create_profile(mac_address)
        # print success, message, data
        return success, message, data

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

game = GameWorld()

game.start()

def game_update():
    game.tick()
    send_data()

if __name__ == '__main__':
    callback_webapp = cyclone.web.Application([
        (r"/profile", ProfileHandler)
    ])

    from autobahn.twisted.websocket import WebSocketServerFactory
    websocket_service = WebSocketServerFactory()
    websocket_service.protocol = ChannelServerProtocol

#subscription = LoopingCall(send_data)
#subscription.start(0.1)

    data_update = LoopingCall(game_update)
    data_update.start(0.5)
    
    # data_update = LoopingCall(fetch_info)
    # data_update.start(0.5)
    fetch_info()

    reactor.listenTCP(9001, websocket_service)
    reactor.listenTCP(5001, callback_webapp, interface="0.0.0.0")

    reactor.run()