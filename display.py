import unicornhathd
import random
import numpy as np
from PIL import Image

width, height = unicornhathd.get_shape()

class Point:
  def __init__(self):
      self.position = np.zeros(2)
      self.color = np.array([255.0,255.0,255.0]) # Default to white.

class Display:
    """Functions for display modes."""
    def __init__(self):
        self.points = []
        self.step = 0
        self.axis = 0

    def InitializeDefault(self, n_points):
        """Randomly initialize points on the matrix."""
        self.points = []
        for p in range(n_points):
            p = Point()
            p.position = np.array([random.randint(0,15), random.randint(0,15)])
            p.color *= random.random()
            self.points.append(p)

    def UpdateAndGetDefaultPoints(self):
        """Update and return points for default display"""
        for p in self.points:
            p.color -= 1
            if p.color[0] <= 0:
                p.color = np.array([200.0,200.0,200.0])*random.random()
                p.position = np.array([random.randint(0,15), random.randint(0,15)])
        return self.points

    def GetImagePixels(self):
        """Returns image pixels for the current image and offset."""
        self.points = []

        for x in range(width):
            for y in range(height):
                pixel = self.img.getpixel((x, y))
                if pixel:
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        p = Point()
                        p.position = np.array([y,x])
                        # Store color but cap brightnes.
                        p.color = np.array([min(r,180), min(g,180), min(b,180)])
                        self.points.append(p)
        return self.points

    def ScrollImage(self, img_file, scroll_axis, scroll_direction, img_transpose):
        """Scrolls image one row of pixels in provided direction.

        Args:
          img_file: String file name for image to show.
          axis: Integer 0 (x-axis) or 1 (y-axis) for scroll axis.
          positive: Boolean indicating scroll direction.
        """
        self.img = Image.open(img_file)
        self.step += scroll_direction
        self.axis = scroll_axis

        # Convert to numpy array and return cropped image.
        np_image = np.array(self.img)
        np_image = np.roll(np_image, self.step, self.axis)[:16,:16]

        self.img = Image.fromarray(np_image)
        self.img = self.img.transpose(img_transpose)

        return self.GetImagePixels()
