#!/usr/bin/env python
import os.path
import signal
import sys
import math
import time
import colorsys
import buttonshim
import unicornhathd
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from PIL import Image
from enum import Enum

import display

MQTT_NEIGHBOR = "clubhouse.local"  # Set this to the hostname of the other display.
MQTT_PATH = "comms_channel"

# Set path of images passed to display.
my_path = os.path.abspath(os.path.dirname(__file__))
ghost_path = os.path.join(my_path, "ghost_tall.png")

class Mode(Enum):
    DEFAULT = 0
    GHOST = 1
    GLASSES = 2

def main():
    """Main function for displaying different modes."""

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

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    publish.single(MQTT_PATH, Mode.DEFAULT, hostname=MQTT_NEIGHBOR)

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    publish.single(MQTT_PATH, Mode.GHOST, hostname=MQTT_NEIGHBOR)

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    publish.single(MQTT_PATH, Mode.GLASSES, hostname=MQTT_NEIGHBOR)

# The callback for when a PUBLISH message is received from the neighbor.
def on_message(client, userdata, msg):
    global mode
    mode = msg.payload

def signal_handler(sig, frame):
    client.loop_stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Configure and start MQTT client.
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_NEIGHBOR)
client.loop_start()

# Configure Unicorn hat display.
unicornhathd.rotation(0)
unicornhathd.brightness(0.6)

# Initialize Display class.
display = display.Display()

# Set default mode.
mode = Mode.DEFAULT

main()
