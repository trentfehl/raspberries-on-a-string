#!/usr/bin/env python
import signal
import math
import time
import colorsys
import buttonshim
import unicornhathd
import PIL

from enum import Enum

import display

class Mode(Enum):
    DEFAULT = 0
    GHOST = 1

def main():
    """Main function for displaying different modes."""

    while True:
        display.InitializeDefault(n_points = 20)
        while mode == Mode.DEFAULT:
            unicornhathd.clear()
            points = display.UpdateAndGetDefaultPoints()
            for p in points:
                unicornhathd.set_pixel(p.position[0], p.position[1],
                                       p.color[0], p.color[1], p.color[2])
            unicornhathd.show()
            time.sleep(0.01)

        while mode == Mode.GHOST:
            unicornhathd.clear()
            unicornhathd.show()

            points = display.ScrollImage(img_file="ghost_tall.png",
                                         scroll_axis=0,
                                         scroll_direction=-1,
                                         img_transpose=PIL.Image.ROTATE_180)
            for p in points:
                unicornhathd.set_pixel(p.position[0], p.position[1],
                                       p.color[0], p.color[1], p.color[2])
            unicornhathd.show()
            time.sleep(0.005)

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

main()
