import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid, mou_pos
from random import randint as ri
from math import sin, cos
import numpy as np

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def len(self):
        return np.linarg.norm([self.x, self.y])

    def rot(self, ang):
        r = self.len()
        self.x = r*cos(ang)
        self.y = r*sin(ang)

class Vector2(Vector):
    def __init__(self, x, y, x2, y2):
        """
        x, y, x2, y2
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
        r = self.len()
        self.x2 = self.x + r*cos(ang)
        self.y2 = self.y + r*sin(ang)

class Boundary:
    def __init__(self, x1, y1, x2, y2):
        global pd
        #self.a = Vector(x1, y1)
        #self.b = Vector(x2, y2)
        self.a = Vector2(x1, y1, x2, y2)
        self.pd = pd

    def show(self):
        self.pd.line((self.a.x, self.a.y), (self.a.x2, self.a.y2))

    def rot(self, ang):
        self.a.rot(ang)

class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = Vector2()

    '''def lookAt(x, y):
    this.dir.x = x - this.pos.x
    this.dir.y = y - this.pos.y
    this.dir.normalize()

  show() {
    stroke(255);
    push();
    translate(this.pos.x, this.pos.y);
    line(0, 0, this.dir.x * 10, this.dir.y * 10);
    pop();

  cast(wall) {
    const x1 = wall.a.x;
    const y1 = wall.a.y;
    const x2 = wall.b.x;
    const y2 = wall.b.y;

    const x3 = this.pos.x;
    const y3 = this.pos.y;
    const x4 = this.pos.x + this.dir.x;
    const y4 = this.pos.y + this.dir.y;

    const den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
    if (den == 0) {
      return;
    }

    const t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den;
    const u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den;
    if (t > 0 && t < 1 && u > 0) {
      const pt = createVector();
      pt.x = x1 + t * (x2 - x1);
      pt.y = y1 + t * (y2 - y1);
      return pt;
    } else {
      return;
    }
  }'''

def make_walls(w, h, wall_num):
    return [Boundary(ri(0, w), ri(0, h), ri(0, w), ri(0, h)) for i in range(wall_num)]

pd = pyg_draw(2)
w, h = pd.scr
num = 0
walls = make_walls(w, h, num)
b = make_walls(w, h, 1)[0]
run = True
c = 0
while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            if event.key == K_r:
                walls = make_walls(w, h, num)
                b = make_walls(w, h, 1)[0]

    for wall in walls:
        wall.show()

    #b.rot(c)
    b.show()

    pd.upd()
    pd.fill()
    c += 0.001
