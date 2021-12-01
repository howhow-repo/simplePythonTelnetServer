#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver, sys, threading
from time import ctime


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        cur = threading.current_thread()
        peer_name = self.request.getpeername()
        print(f'[{ctime()}] Client connected from {self.request.getpeername()} and [{cur.name}] is handling with him.')
        self.request.send(str.encode("You can close thisd connection by ctrl+c or 'exit':\n"))
        self.request.send(str.encode("<<<< sent: "))
        while True:
            try:
                indata = self.request.recv(1024).strip()
                if indata == b'\xff\xf4\xff\xfd\x06' or indata.decode() == 'exit':  # connection closed
                    self.request.close()
                    print('client closed connection.')
                    break
                print(f'{peer_name} rev: {indata.decode()}')

                outdata = f'>>>> resp: echo: {indata.decode()}\n'\
                          f'<<<< sent: '

                self.request.send(outdata.encode())
            except ConnectionResetError:
                print(f"---- {peer_name} Connection reset by peer, exit thread ----")
                break
            except BrokenPipeError:
                print(f"---- {peer_name} Broken pipe, exit thread ----")
                break
            except OSError as e:
                print(f"{e}")
                break


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
