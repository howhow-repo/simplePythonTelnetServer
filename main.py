#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver, sys, threading
import logging
from time import ctime

from indata_handler import IndataHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    output_template = '>> resp: {resp}\n\n'\
                      '<< sent: '

    def handle(self):
        cur = threading.current_thread()
        peer_name = self.request.getpeername()
        logger.info(f'[{ctime()}] Client connected from {self.request.getpeername()}; [{cur.name}] is handling.')
        self.request.send(str.encode("You can close thisd connection by ctrl+c or 'exit':\n\n"))
        self.request.send(str.encode("<< sent: "))
        while True:
            try:
                indata = self.request.recv(1024).strip()

                if indata == b'\xff\xf4\xff\xfd\x06'\
                        or indata.decode() == 'exit':  # ctrl+c or 'exit' make connection closed
                    self.request.close()
                    logger.info(f'---- {peer_name}, client closed connection. ----')
                    break

                logger.info(f'{peer_name} rev: {indata.decode()}')
                outdata = self.output_template.format(resp=IndataHandler.reaction(indata))
                self.request.send(outdata.encode())

            except ConnectionResetError:
                logger.info(f"---- {peer_name} Connection reset by peer, exit thread ----")
                break
            except BrokenPipeError:
                logger.warning(f"---- {peer_name} Broken pipe, exit thread ----")
                break
            except OSError as e:
                logger.error(f"{e}")
                break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 7000
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    logger.info(f'server start at: {HOST}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
