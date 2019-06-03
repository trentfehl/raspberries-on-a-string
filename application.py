#!/usr/bin/env python
import signal
import math
import time
import colorsys
import buttonshim
import unicornhathd

def display_default():
    ShowDisplay = True

    unicornhathd.rotation(0)
    unicornhathd.brightness(0.6)

    step = 0
    try:
	while ShowDisplay:
	    step += 1
	    for x in range(0, 16):
		for y in range(0, 16):
		    dx = 7
		    dy = 7

		    dx = (math.sin(step / 20.0) * 15.0) + 7.0
		    dy = (math.cos(step / 15.0) * 15.0) + 7.0
		    sc = (math.cos(step / 10.0) * 10.0) + 16.0

		    h = math.sqrt(math.pow(x - dx, 2) + math.pow(y - dy, 2)) / sc

		    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)

		    r *= 255.0
		    g *= 255.0
		    b *= 255.0

		    unicornhathd.set_pixel(x, y, r, g, b)

	    unicornhathd.show()
	    time.sleep(1.0 / 60)

    except KeyboardInterrupt:
	unicornhathd.off()

def display_happy():
    ShowDisplay = True

    unicornhathd.brightness(0.6)

    try:
	while ShowDisplay:
	    for rotation in [0, 90, 180, 270]:
		print('Showing lines at rotation: {}'.format(rotation))

		unicornhathd.clear()
		unicornhathd.rotation(rotation)
		unicornhathd.set_pixel(0, 0, 64, 64, 64)
		unicornhathd.show()
		time.sleep(0.5)

		for x in range(1, 16):
		    unicornhathd.set_pixel(x, 0, 255, 0, 0)
		    unicornhathd.show()
		    time.sleep(0.5 / 16)

		time.sleep(0.5)

		for y in range(1, 16):
		    unicornhathd.set_pixel(0, y, 0, 0, 255)
		    unicornhathd.show()
		    time.sleep(0.5 / 16)

		time.sleep(0.5)

		for b in range(1, 16):
		    unicornhathd.set_pixel(b, b, 0, 255, 0)
		    unicornhathd.show()
		    time.sleep(0.5 / 16)

		time.sleep(0.5)

    except KeyboardInterrupt:
	unicornhathd.off()

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    # Reset display.
    global ShowDisplay
    ShowDisplay = False

    display_default()

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    # Reset display.
    global ShowDisplay
    ShowDisplay = False

    display_happy()

signal.pause()
