#!/usr/bin/env python
import argparse
import signal
import sys
import socket
import buttonshim
from enum import IntEnum

parser = argparse.ArgumentParser()
parser.add_argument("loopback")
args = parser.parse_args()

class Mode(IntEnum):
    DEFAULT = 0
    DROPS = 1
    GHOST = 2
    GLASSES = 3

class ButtonWriter(object):

    # Change the host to match the IP address to match the connected device.
<<<<<<< HEAD
    def __init__(self, host='192.168.1.11', port=9000):
=======
    # Ex: def __init__(self, host='192.168.1.11', port=9001):
    def __init__(self, host='192.168.1.10', port=9001):
>>>>>>> fc1f7354759f7fad678c347bbd72bfb0364bf144
        self._sock = socket.create_connection((host, port))

    def send(self, data):
        self._sock.sendall(data)

local_writer = ButtonWriter("localhost", 9001)

if args.loopback:
  writer = local_writer
else:
  writer = ButtonWriter()

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    writer.send(Mode.DEFAULT.name.encode())

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    writer.send(Mode.DROPS.name.encode())

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    writer.send(Mode.GHOST.name.encode())

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    writer.send(Mode.GLASSES.name.encode())

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    local_writer.send(Mode.DEFAULT.name.encode())


def signal_handler(sig, frame):
    sys.exit(0)

buttonshim.set_pixel(0x00, 0x00, 0x00)
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
