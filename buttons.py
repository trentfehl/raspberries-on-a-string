#!/usr/bin/env python
import signal
import sys
import socket
import buttonshim
from enum import IntEnum

class Mode(IntEnum):
    DEFAULT = 0
    GHOST = 1
    GLASSES = 2

class ButtonWriter(object):

    # Change the host to match the IP address to match the connected device.
    # Ex: def __init__(self, host='192.168.1.11', port=9001):
    def __init__(self, host='192.168.1.10', port=9001):
        self._sock = socket.create_connection((host, port))

    def send(self, data):
        self._sock.sendall(data)

writer = ButtonWriter()

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    writer.send(Mode.DEFAULT.name.encode())

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    writer.send(Mode.GHOST.name.encode())

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    writer.send(Mode.GLASSES.name.encode())

def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
