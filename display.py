import unicornhathd
import random
import numpy as np

class Point:
  def __init__(self):
      self.position = np.zeros(2)
      self.color = np.array([255.0,255.0,255.0]) # Default to white.

class Display:
    """Functions for display modes."""
    def __init__(self):
        self.points = []

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

