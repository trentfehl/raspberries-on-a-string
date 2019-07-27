#!/usr/bin/env python
import signal
import sys
import buttonshim

class ButtonWriter(object):

    def __init__(self, host='localhost', port=8080):
        self._sock = socket.create_connection((host, port))

    def send(self, data):
        self._sock.sendall(data)

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    writer = ButtonWriter()
    writer.send(Mode.DEFAULT)

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    writer = ButtonWriter()
    writer.send(Mode.GHOST)

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    writer = ButtonWriter()
    writer.send(Mode.GLASSES)

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
