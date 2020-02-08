import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid, mou_pos
from random import randint as ri

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def len(self):
        return np.linarg.norm([self.x, self.y])

class Vector2(Vector):
    def __init__(self, x, y, x2, y2):
        Vector.__init__(self, x, y)
        self.x2 = x2
        self.y2 = y2

    def len(self):
        return np.linarg.norm([self.x2-self.x, self.y2-self.y])

class Boundary:
    def __init__(self, x1, y1, x2, y2):
        global pd
        #self.a = Vector(x1, y1)
        #self.b = Vector(x2, y2)
        self.a = Vector2(x1, y1, x2, y2)
        self.pd = pd

    def show(self):
        self.pd.line((self.a.x, self.a.y), (self.a.x2, self.a.y2))

class Ray:
  def __init__(self, pos, angle):
    self.pos = pos
    self.dir = p5.Vector.fromAngle(angle)

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

pd = pyg_draw(2)
w, h = pd.scr
b = Boundary(ri(0, w), ri(0, w), ri(0, h), ri(0, h))
run = True
while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False

    b.show()

    pd.upd()
    pd.fill()
