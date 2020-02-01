import pygame
from pygame.locals import *
#import imp#ortlib as imp
#import sys
#import os
#print(sys.path)
#for i in sys.path:
#    try:
#        d = os.path.join(i, "pygame_draw.py")
#        imp.load_source('pygame_draw', d)
#        print(43)
#    except Exception: pass
from pygame_draw import pyg_draw, Grid
from random import randint as ri
from numpy.random import randint as nri
import numpy as np
from math import sin, cos, sqrt, pi, tau

def trans(x, y, r, ang):
    x += r*cos(ang)
    y += r*sin(ang)
    return (x, y)

def cone(pd, x, y, r, ang, view, num):
    rec = [x-r, y-r, r*2, r*2]
    pd.arc("green", rec, -ang-view, -ang+view)
    pd.rect("blue", rec, 1)
    for t in range(num):
        pd.line("green", (x, y), trans(x, y, r, ang+t/(num-1)-view), 2)
    
def check(arr, self):
    row, col = self.row, self.col
    x, y = self.x, self.y
    mx, my = self.mx, self.my
    fx, fy = x-mx, y-my
    for i in range(row):
        for j in range(col):
            p1 = x*i+mx/2
            p2 = y*j+my/2
            [p1, p2, fx, fy]

num = 2**0

pd = pyg_draw(2)
gr = Grid(pd, num)

siz = (gr.row, gr.col)

grids = np.full(siz, 0)

map = np.array([
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 1, 1]])
      
msz = map.shape     
ang = 0
qual = 10
view = 1/2
max_d = 100
x, y = 1.5*gr.x, 1.5*gr.y
sx, sy = 0, 0
run = True
while run:
    #grids = nri(0, 3, siz)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
                
            if event.key == K_z:
                ang -= 1/2
            if event.key == K_x:
                ang += 1/2
                
    grids[sx:sx+msz[1], sy:sy+msz[0]] = np.rot90(map)[::-1]
    gr.draw(grids)
                  
    cone(pd, x, y, max_d, ang, view, qual)
    #pd.circ("red", (x, y), 10)
                                    
    pd.upd()
    pd.fill("black")