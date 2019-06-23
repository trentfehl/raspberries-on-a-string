#!/usr/bin/env python
import signal
import math
import time
import colorsys
import buttonshim
import unicornhathd
from PIL import Image

from enum import Enum

import display

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

            points = display.UpdateImage(img_file="ghost_tall.png",
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
    mode = Mode.GHOST

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global mode
    mode = Mode.GLASSES

main()
