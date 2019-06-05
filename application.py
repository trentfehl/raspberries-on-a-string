#!/usr/bin/env python
import signal
import math
import time
import colorsys
import buttonshim
import unicornhathd

from enum import Enum

import display

class Mode(Enum):
    DEFAULT = 0
    HAPPY = 1

def main():
    """Main function for displaying different modes."""

    while True:
        unicornhathd.clear()
        points = display.initialize_default()
        while mode == Mode.DEFAULT:
            for p in points:
                unicornhathd.set_pixel(p["x"], p["y"], p["r"], p["g"], p["b"])
            points = display.update_default()
            
        unicornhathd.clear()
        points = display.initialize_happy()
        while mode == Mode.HAPPY:
            for p in points:
                unicornhathd.set_pixel(p["x"], p["y"], p["r"], p["g"], p["b"])
            points = display.update_happy()

mode = Mode.DEFAULT
unicornhathd.rotation(0)
unicornhathd.brightness(0.6)

display = Display()

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global mode
    mode = Mode.DEFAULT

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global mode
    mode = Mode.HAPPY

main()
