import unicornhathd
import colorsys
import random
import time
import numpy as np
from PIL import Image
import os.path
from itertools import permutations

my_path = os.path.abspath(os.path.dirname(__file__))
glasses_path = os.path.join(my_path, "glasses.png")

width, height = unicornhathd.get_shape()

class Point:
  def __init__(self, position=None):
      self.position = np.zeros(2) if position is None else position
      self.color = np.array([255.0,255.0,255.0]) # Default to white.

class Display:
    """Functions for display modes."""
    def __init__(self):
        self.points = []
        self.step = 0
        self.axis = 0

    def InitializeRandomPoints(self, n_points):
        """Randomly initialize points on the matrix."""
        self.points = []
        for p in range(n_points):
            p = Point()
            p.position = np.array([random.randint(0,15), random.randint(0,15)])
            p.color *= random.random()
            self.points.append(p)

    def UpdateRandomPoints(self):
        """Update and return points for default display."""
        for p in self.points:
            p.color -= 1
            if p.color[0] <= 0:
                p.color = np.array([200.0,200.0,200.0])*random.random()
                p.position = np.array([random.randint(0,15), random.randint(0,15)])
        return self.points

    def GetDropletPoints(self, p_center):
        """Generate points for a droplet."""
        droplet = []

        # Add center point to the droplet.
        droplet.append([p_center])

        # Generate points for waves emanating from center point.
        for wave in [1,2,3]:
          points = []

          for offset in permutations(list(range(wave, -wave)), 2):
            if abs(wave) in offset:
              points.append(Point(position=(p_center.position+offset)))
          droplet.append(points)

        return droplet

    def UpdateDroplets(self):
        """Update and return droplets."""
        droplet_points = []

        for p in self.points:
          droplet = self.GetDropletPoints(p)
          h = random.uniform(0,1)     # Hue.
          v = np.zeros(len(droplet))  # Brightness for each wave.
          v[0] = 1                    # Make center point brightness high.
          v[1] = 1
          v[2] = 1

          for index, wave in enumerate(droplet):
            r, g, b = colorsys.hsv_to_rgb(h, 1, v[index])

            r *= 255.0
            g *= 255.0
            b *= 255.0

            for point in wave:
              v[index] -= 0.01
              point.color = np.array([r,g,b])
            droplet_points.append(point)

            if v[index] <= 0:
                p.position = np.array([random.randint(0,15), random.randint(0,15)])

        return droplet_points

    def GetImagePoints(self):
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

    def UpdateImage(self, img_file, scroll_params, img_transpose):
        """Scrolls image one row of pixels in provided direction.

        Args:
          img_file: String file name for image to show.
          scroll_params: Tuple containing scroll axis and scroll step.
          img_transpose: PIL image transpose Enum.
        """
        self.img = Image.open(img_file)
        self.axis = scroll_params[0]
        self.step += scroll_params[1]

        # Convert to numpy array and return cropped image.
        np_image = np.array(self.img)
        np_image = np.roll(np_image, self.step, self.axis)[:16,:16]

        self.img = Image.fromarray(np_image)
        self.img = self.img.transpose(img_transpose)

        return self.GetImagePoints()

    def UpdateGlassesImage(self):
        if self.step >= 10 or self.step < 0:
          time.sleep(1.5)
          self.step = 0

        time.sleep(0.1)
        return self.UpdateImage(glasses_path, (0, 1), Image.ROTATE_180)
