#!/usr/bin/env python
import os.path
import signal
import socket
import asyncore
import threading
import sys
import math
import time
import colorsys
import unicornhathd
from enum import Enum
from PIL import Image

import display_lib

# Set path of images passed to display.
my_path = os.path.abspath(os.path.dirname(__file__))
ghost_path = os.path.join(my_path, "ghost_tall.png")

# Configure Unicorn hat display.
unicornhathd.rotation(0)
unicornhathd.brightness(0.6)

def signal_handler(sig, frame):
    sys.exit(0)

class Mode(Enum):
    DEFAULT = 0
    GHOST = 1
    GLASSES = 2

class DisplayServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)

        self._thread = None
        self._read_handler = None

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def start(self):
        """
        For use when an asyncore.loop is not already running.
        Starts a threaded loop.
        """
        if self._thread is not None:
            return

        self._thread = threading.Thread(target=asyncore.loop, kwargs={'timeout':1})
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        """Stops a threaded loop"""
        self.close()
        if self._thread is not None:
            thread, self._thread = self._thread, None
            thread.join()

    def set_read_handler(self, read_fn):
        """
        Set a callable function that accepts a socket which is
        ready for data to be read
        """
        if not callable(read_fn):
            raise TypeError('read_fn %r is not callable' % read_fn)

        class Handler(asyncore.dispatcher_with_send):
            def handle_read(self):
                read_fn(self)

        self._read_handler = Handler

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return

        sock, addr = pair
        if self._read_handler is None:
            print('No read handler. Refusing connection from %s' % repr(addr))
            sock.close()
            return

        print('Incoming connection from %s' % repr(addr))
        self._read_handler(sock)

class DisplayHandler(object):

    def __init__(self, host='0.0.0.0', port=9000):
        self.server = DisplayServer(host, port)
        self.server.set_read_handler(self.handle_read)
        self.server.start()

    def handle_read(self, sock):
        data = sock.recv(8192)
        if data:
          global mode
          mode = Mode[data.decode()]
          print("mode = {}".format(mode))

def main():
    """Main function for displaying different modes."""
    server = DisplayHandler()

    # Set starting mode.
    global mode
    mode = Mode.DEFAULT

    # Initialize Display class.
    display = display_lib.Display()

    while True:
        display.InitializeRandomPoints(n_points = 20)
        while mode == Mode.DEFAULT:
            unicornhathd.clear()
            points = display.UpdateRandomPoints()
            for p in points:
                unicornhathd.set_pixel(p.position[0], p.position[1],
                                       p.color[0], p.color[1], p.color[2])
            unicornhathd.show()
            time.sleep(0.01)

        while mode == Mode.GHOST:
            unicornhathd.clear()
            unicornhathd.show()

            points = display.UpdateImage(img_file=ghost_path,
                                         scroll_params=(0, -1),
                                         img_transpose=Image.ROTATE_180)
            for p in points:
                unicornhathd.set_pixel(p.position[0], p.position[1],
                                       p.color[0], p.color[1], p.color[2])
            unicornhathd.show()
            time.sleep(0.005)

        points = display.UpdateGlassesImage()
        while mode == Mode.GLASSES:
            unicornhathd.clear()
            unicornhathd.show()

            for p in points:
                unicornhathd.set_pixel(p.position[0], p.position[1],
                                       p.color[0], p.color[1], p.color[2])
            unicornhathd.show()
            time.sleep(0.005)
            points = display.UpdateGlassesImage()


main()
