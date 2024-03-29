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
        return np.linalg.norm([self.x, self.y])

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

    def rot(self, ang, add=0):
        self.a.rot(ang)

class Ray(Boundary):
    def __init__(self, x, y, ang):
        self.a = Vector2(x, y, x, y+10)
        self.ang = ang
        self.a.rot(ang)

    def cast(self, wall):
        x1, y1 = wall.a.x, wall.a.y
        x2, y2 = wall.a.x2, wall.a.y2

        x3, y3 = self.a.x, self.a.y
        x4, y4 = self.a.x2, self.a.y2

        det = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

        #if det != 0:
        #    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/det
        #    u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/det

        #    if 0 <= t <= 1 and 0 <= u:
        #        return [x1+t*(x2-x1), y1+t*(y2-y1)]
        #    else:
        #        return None
        #else:
        #    return None

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
          return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if 0 < t < 1 and 0 < u:
            return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]
        else:
            return None

    def set(self, x, y):
        self.a.x = x
        self.a.y = y
        self.a.x2 = x
        self.a.y2 = y+10
        self.a.rot(self.ang)

    def rot(self, ang, add=0):
        if add != 0:
            self.a.rot(ang+self.ang)
        else:
            self.a.rot(ang)

class Particle:
    def __init__(self, ang, view):
        global w, h
        self.pos = Vector(w/2, h/2)
        self.rays = [Ray(self.pos.x,self.pos.y, radians(a)) for a in range(ang-view, ang+view, 1)]
            
    def __init__(self, ang, view):
        self.rays = [Ray(self.pos.x,self.pos.y, radians(a)) for a in range(ang-view, ang+view, 1)]

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y
        for ray in self.rays:
            ray.set(x, y)
        #self.rays = [Ray(x, y, radians(a)) for a in range(0, 361, 1)]

    def look(self, walls):
        global pd
        for ray in self.rays:
            closest = None
            record = float("inf")
            for wall in walls:
                p = ray.cast(wall)
                if p != None:
                    d = Vector2(*p, ray.a.x, ray.a.y).len()
                    if d < record:
                        record = d
                        closest = p
            if closest != None:
                pd.line((ray.a.x, ray.a.y), [*closest])

    def show(self):
        global pd
        pd.circ((self.pos.x, self.pos.y), 4)
        for ray in self.rays:
            pass#ray.show()

'''class Particle {

  updateFOV(fov) {
    this.fov = fov;
    this.rays = [];
    for (let a = -this.fov / 2; a < this.fov / 2; a += 1) {
      this.rays.push(new Ray(this.pos, radians(a) + this.heading));
    }
  }

  rotate(angle) {
    this.heading += angle;
    let index = 0;
    for (let a = -this.fov / 2; a < this.fov / 2; a += 1) {
      this.rays[index].setAngle(radians(a) + this.heading);
      index++;
    }
  }

  move(amt) {
    const vel = p5.Vector.fromAngle(this.heading);
    vel.setMag(amt);
    this.pos.add(vel);
  }

  update(x, y) {
    this.pos.set(x, y);
  }

  look(walls) {
    const scene = [];
    for (let i = 0; i < this.rays.length; i++) {
      const ray = this.rays[i];
      let closest = null;
      let record = Infinity;
      for (let wall of walls) {
        const pt = ray.cast(wall);
        if (pt) {
          let d = p5.Vector.dist(this.pos, pt);
          const a = ray.dir.heading() - this.heading;
          //if (!mouseIsPressed) {
            d *= cos(a);
          //}
          if (d < record) {
            record = d;
            closest = pt;
          }
        }
      }
      if (closest) {
        // colorMode(HSB);
        // stroke((i + frameCount * 2) % 360, 255, 255, 50);
        stroke(255, 100);
        line(this.pos.x, this.pos.y, closest.x, closest.y);
      }
      scene[i] = record;
    }
    return scene;
  }

  show() {
    fill(255);
    ellipse(this.pos.x, this.pos.y, 4);
    for (let ray of this.rays) {
      ray.show();
    }
  }
}'''


def make_walls(w, h, wall_num):
    return [Boundary(ri(0, w), ri(0, h), ri(0, w), ri(0, h)) for i in range(wall_num)]

pd = pyg_draw(2)
mou = mou_pos(pd)
md = mou.mang
mp = mou.mpos
w, h = pd.scr
#h//=2
num = 5

walls = []
walls = make_walls(w, h, num)
walls.append(Boundary(-1, -1, w, -1))
walls.append(Boundary(w, -1, w, h))
walls.append(Boundary(w, h, -1, h))
walls.append(Boundary(-1, h, -1, -1))
particle = Particle()

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

    particle.update(*mp(cent=0))
    particle.show()
    particle.look(walls)

    pd.upd()
    pd.fill()
