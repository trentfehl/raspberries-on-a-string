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
        display.InitializeDefault(n_points = 20)
        while mode == Mode.DEFAULT:
            unicornhathd.clear()
            points = display.UpdateAndGetDefaultPoints()
            time.sleep(0.01)
            for p in points:
                unicornhathd.set_pixel(p.position[0], p.position[1],
                                       p.color[0], p.color[1], p.color[2])
            unicornhathd.show()
            
        """
        unicornhathd.clear()
        points = display.InitializePoints(n_points = 6)
        while mode == Mode.HAPPY:
            points = display.GetPoints()
            for p in points:
                unicornhathd.set_pixel(p.x, p.y, p.r, p.g, p.b)
            points = display.UpdateHappy()
        """

mode = Mode.DEFAULT
unicornhathd.rotation(0)
unicornhathd.brightness(0.6)

display = display.Display()

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global mode
    mode = Mode.DEFAULT

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global mode
    mode = Mode.HAPPY

main()
