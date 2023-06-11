from __future__ import print_function, division
from math       import sqrt

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def dist(self, other):
        return (self - other).magnitude()
    
    def unpack(self):
        return (self.x, self.y, self.z)