import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid, mou_pos
from random import randint as ri
from math import sin, cos, radians, atan2
import numpy as np

class Vector:
    def __init__(self, x, y):
        """
        init vector
        """
        self.x = x
        self.y = y

    def len(self):
        """
        calculate vector length
        """
        return np.linarg.norm([self.x, self.y])

    def rot(self, ang):
        """
        rotates the vector by a given angle
        """
        r = self.len()
        self.x = r*cos(ang)
        self.y = r*sin(ang)

class Vector2(Vector):
    def __init__(self, x, y, x2, y2):
        """
        init vector2
        """
        Vector.__init__(self, x, y)
        self.x2 = x2
        self.y2 = y2

    def len(self):
        """
        calculate vector length
        """
        return np.linalg.norm([self.x2-self.x, self.y2-self.y])

    def rot(self, ang):
        """
        rotates the vector by a given angle around the beginning of the vector
        """
        r = self.len()
        self.x2 = self.x + r*cos(ang)
        self.y2 = self.y + r*sin(ang)

class Boundary:
    def __init__(self, x1, y1, x2, y2):
        self.a = Vector2(x1, y1, x2, y2)

    def show(self):
        global pd
        pd.line((self.a.x, self.a.y), (self.a.x2, self.a.y2))

    def rot(self, ang):
        self.a.rot(ang)

class Ray(Boundary):
    def __init__(self, x, y, ang):
        self.a = Vector2(x, y, x, y+10)
        self.a.rot(ang)

    def cast(self, wall):
        x1, y1 = wall.a.x, wall.a.y
        x2, y2 = wall.a.x2, wall.a.y2

        x3, y3 = self.a.x, self.a.y
        x4, y4 = self.a.x2, self.a.y2

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
          return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if 0 < t < 1 and u > 0:
            pt = Vector(x1 + t * (x2 - x1),
                        y1 + t * (y2 - y1))
            return pt
        else:
            return None

def make_walls(w, h, wall_num):
    return [Boundary(ri(0, w), ri(0, h), ri(0, w), ri(0, h)) for i in range(wall_num)]

pd = pyg_draw(2)
mou = mou_pos(pd)
md = mou.mang
w, h = pd.scr
num = 5
walls = make_walls(w, h, num)
v = Ray(w/2, h/2, radians(0))

run = True
c = 0
while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_r:
                walls = make_walls(w, h, num)

    for wall in walls:
        wall.show()

    v.show()
    v.rot(md())

    pd.upd()
    pd.fill()
