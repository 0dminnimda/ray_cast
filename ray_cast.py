import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid
from random import randint as ri
from numpy.random import randint as nri
import numpy as np
from math import sin, cos, sqrt, pi, tau

def trans(x, y, r, ang):
    x += r*cos(ang)
    y += r*sin(ang)
    return (x, y)

def cone(pd, x, y, max, ang, view):
    pos = trans(x, y, max_d, ang)
    hm = max
    rec = [x-hm, y-hm, max*2, max*2]
    #pd.arc("green", rec, ang-view/2, ang+view/2)
    pd.line("green", (x, y), pos)
    #pd.rect("blue", rec, 5)
    for t in range(int(ang-view/2), int(ang+view/2)):
        pd.circ("green", trans(x, y, max, t), 10)
    
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

pd = pyg_draw(1)
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
view = 1
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
                ang -= 1/4
            if event.key == K_x:
                ang += 1/4
                
    grids[sx:sx+msz[1], sy:sy+msz[0]] = np.rot90(map)[::-1]
    gr.draw(grids)
                  
    cone(pd, x, y, max_d, ang, view)
    pd.circ("red", (x, y), 10)
                                    
    pd.upd()
    pd.fill("black")