#!/usr/bin/env python
__author__ = 'mark'
import sys
import json

import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.tcpserver
import tornado.iostream

from cache import mc

sys.path.append('pycharm-debug-py3k.egg')
DEBUGGER_IP = '31.148.105.80'
tcp_connection = None


class WSConnectionPool(object):
    instance = None
    connection_pool = dict()

    def __new__(cls, *args):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def send_notification(self, notification):
        users = notification['users']
        del notification['users']
        if (notification['type'] == 'message') or (notification['type'] == 'friends_proposal'):
            for user_id in users:
                try:
                    for connection in self.connection_pool[user_id]:
                        connection.ws_connection.write_message(json.dumps(notification))
                except KeyError:
                    pass
            else:
                pass

    def append(self, user_id, connection):
        if user_id in self.connection_pool:
            self.connection_pool[user_id].append(connection)
        else:
            self.connection_pool[user_id] = list()
            self.connection_pool[user_id].append(connection)

    def __getitem__(self, key):
        return self.connection_pool[key]


class WebSocket(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        self.ws_connection.write_message('get sess_id')
        pass

    def on_message(self, message):
        try:
            request = json.loads(message)
            sess_id = request['sess_id']
            user_id = mc.get_user_id('MR.sessId_', sess_id)
            if user_id != 0:
                ws_cp = WSConnectionPool()
                ws_cp.append(user_id, self)
                self.current_user = user_id
        except Exception as e:
            pass
        return 0

    def on_close(self):  # Garbage collector
        ws_cp = WSConnectionPool()
        if self.current_user:
            for connection_key in range(len(ws_cp[self.current_user])):
                if not ws_cp[self.current_user][connection_key].ws_connection:
                    del ws_cp[self.current_user][connection_key]
        del self

    def check_origin(self, origin):
        return True


class TCPServer(tornado.tcpserver.TCPServer):

    def handle_stream(self, stream, address):
        stream.read_until_close(self.message_handler, self.message_handler)

    def message_handler(self, data):
        ws_cp = WSConnectionPool()
        try:
            notification = json.loads(data.decode())
            ws_cp.send_notification(notification)
        except Exception as e:
            pass

handlers = ((r'/notifications', WebSocket),)
application = tornado.web.Application(handlers)
tcp_server = TCPServer()


if __name__ == '__main__':
    # pydevd.settrace(DEBUGGER_IP, port=32457, stdoutToServer=True, stderrToServer=True)
    application.listen(8888)
    tcp_server.listen(9999)
    io_loop = tornado.ioloop.IOLoop.instance()
    try:
        io_loop.start()
    except KeyboardInterrupt:
        io_loop.stop()