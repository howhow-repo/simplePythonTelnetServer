#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver, sys, threading
from time import ctime


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        cur = threading.current_thread()
        print(f'[{ctime()}] Client connected from {self.request.getpeername()} and [{cur.name}] is handling with him.')
        while True:
            indata = self.request.recv(1024).strip()
            if len(indata) == 0:  # connection closed
                self.request.close()
                print('client closed connection.')
                break
            print(f'rev: {indata.decode()}')

            outdata = f'echo {indata.decode()}\n'
            self.request.send(outdata.encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 7000
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print(f'server start at: {HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
