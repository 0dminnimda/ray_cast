import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid
from random import randint as ri
from numpy.random import randint as nri
import numpy as np
from math import sin, cos, tan, sqrt, pi, tau, atan2

def trans(x, y, r, ang):
    x += r*cos(ang)
    y += r*sin(ang)
    return [x, y]

def cone(pd, me):
    x, y, r = me.x, me.y, me.r
    ang, view, num = me.ang, me.view, me.qual
    rec = [x-r, y-r, r*2, r*2]
    pd.circ("yellow", (x, y), 10)
    pd.rect("blue", rec, 2)
    pd.circ("blue", (x, y), r, 2)
    #pd.arc("green", rec, -ang-view, -ang+view)
    pts = []
    for t in range(num):
        po = trans(0, 0, r, ang-t/(num-1)*view*pi)
        pd.line("green", (x, y), (po[0]+x, po[1]+y), 2)
        pts.append(po)
    return pts

def intersection(a, b):
    x1, y1, x2, y2 = a
    x3, y3, x4, y4 = b

    det = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/det
    u = -((x1-x2)*(y3-y3)-(y1-y2)*(x3-x4))/det

    if 0 <= t <= 1 and 0 <= u <= 1:
        px = x1+t*(x2-x1)
        py = y1+t*(y2-y1)
        return [px, py]
    else:
        return False

def lines(arr):
    pass

def check(arr, gr, me, pd, pts):
    pos = (me.x, me.y)
    row, col = gr.row, gr.col
    x, y = gr.x, gr.y
    mx, my = gr.mx, gr.my
    fx, fy = x-mx, y-my
    for i in range(row):
        for j in range(col):
            p1 = x*i+mx/2
            p2 = y*j+my/2
            p3, p4 = p1+fx, p2+fy
            if p1<pos[0]<p3 and p2<pos[1]<p4:
                pass#pd.rect("red", [p1, p2, fx, fy], 3)
            pd.rect("graY", [p1, p2, fx, fy], 1)

class cha():
    def __init__(self, gr, x, y, view, ang, qual, r):
        self.view = view
        self.ang = ang
        self.qual = qual
        self.r = r
        self.gr = gr
        self.x, self.y = x*gr.x, y*gr.y
        
    def mov(self, x, y):
        self.x += x*self.gr.x
        self.y += y*self.gr.y
        
    def pos(self, x, y):
        self.x = x*self.gr.x
        self.y = y*self.gr.y

num = 1.4

pd = pyg_draw(2)
gr = Grid(pd, num, 0)

qual = 100
view = 1/4
r = 500

me = cha(gr, 4, 4, view, 0, qual, r)

siz = ((gr.row), (gr.col))
grids = np.full(siz, 0)

map = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],])
      
msz = map.shape     
sx, sy = 0, 0
st = 0.1
run = True
grids[sx:sx+msz[1], sy:sy+msz[0]] = np.rot90(map)[::-1]
while run:
    #grids = nri(0, 3, siz)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
                
            if event.key == K_z:
                me.ang -= tau/16
            if event.key == K_x:
                me.ang += tau/16
                
            if event.key == K_w:
                me.mov(0, -st)
            if event.key == K_s:
                me.mov(0, st)
            if event.key == K_a:
                me.mov(-st, 0)
            if event.key == K_d:
                me.mov(st, 0)
    
    gr.draw(grids)
                  
    pts = cone(pd, me)
    check(grids, gr, me, pd, pts)
    #pd.circ("red", (me.x, me.y), 10)
                                    
    pd.upd()
    pd.fill("black")