import math
import numpy as np
from numpy import sin, cos, arccos


class Vector:
    @staticmethod
    def fromNpArray(array):
        return Vector(x=array[0], y=array[1], z=array[2])

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def describe(self, caption=""):
        print(f"{caption}x: {self.x}, y: {self.y}, z: {self.z}")

    def getXYZ(self):
        return self.x, self.y, self.z

    def toNpArray(self):
        return np.array([self.x, self.y, self.z])

    def addVector(self, B, inplace=False):
        if inplace == True:
            self.x += B.x
            self.y += B.y
            self.z += B.z
            return self
        return Vector(self.x + B.x, self.y + B.y, self.z + B.z)

    def subtractVector(self, B, inplace=False):
        if inplace == True:
            self.x -= B.x
            self.y -= B.y
            self.z -= B.z
            return self
        return Vector(self.x - B.x, self.y - B.y, self.z - B.z)

    def invert(self, inplace=False):
        if inplace == True:
            self.x = -self.x
            self.y = -self.y
            self.z = -self.z
            return self
        return Vector(-self.x, -self.y, -self.z)

    def scaleByLength(self, l, inplace=False):
        if inplace == True:
            self.x *= l
            self.y *= l
            self.z *= l
            return self
        else:
            return Vector(self.x * l, self.y * l, self.z * l)

    def distanceFrom(self, B):
        return math.sqrt((B.x - self.x)**2 + (B.y - self.y)**2 + (B.z - self.z)**2)

    def angleBetween(self, B):
        cosine = self.dotProduct(B) / (self.magnitude() * B.magnitude())
        # rounding can push this just outside -1 to 1, and arccos returns NaN there
        cosine = max(-1.0, min(1.0, cosine))
        return arccos(cosine)

    def reflectInVector(self, B):
        v = self.normalise()
        normal = B.normalise()
        return v.subtractVector(normal.scaleByLength(2 * v.dotProduct(normal))).normalise()

    def dotProduct(self, B):
        # returns a single number
        return self.x * B.x + self.y * B.y + self.z * B.z

    def crossProduct(self, B):
        # denoted by A x B, returns a Vector
        return Vector(
            x=self.y*B.z - self.z*B.y,
            y=self.z*B.x - self.x*B.z,
            z=self.x*B.y - self.y*B.x
        )

    def magnitude(self):
        # ||v|| denotes the length of a vector
        dotProduct = self.dotProduct(self)
        return math.sqrt(dotProduct)

    def normalise(self):
        magnitude = self.magnitude()
        return Vector(x=self.x/magnitude, y=self.y/magnitude, z=self.z/magnitude)

    def multiplyByMatrix(self, T):
        return self.fromNpArray(np.matmul(self.toNpArray(), T))

    def rotate(self, angle, inplace=False):
        a, b, c = angle.x, angle.y, angle.z
        R = np.array([
            [cos(c)*cos(b)*cos(a) - sin(c)*sin(a), cos(c)*cos(b)*sin(a) + sin(c)*cos(a), -cos(c)*sin(b)],
            [-sin(c)*cos(b)*cos(a) - cos(c)*sin(a), -sin(c)*cos(b)*sin(a) + cos(c)*cos(a), sin(c)*sin(b)],
            [sin(b)*cos(a), sin(b)*sin(a), cos(b)]
        ])
        V = np.matmul(np.array([self.x, self.y, self.z]), R)
        if inplace == True:
            self = Vector(x=V[0], y=V[1], z=V[2])
        return Vector(x=V[0], y=V[1], z=V[2])