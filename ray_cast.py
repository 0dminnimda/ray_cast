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

def cone(pd, x, y, r, ang, view, num):
    rec = [x-r, y-r, r*2, r*2]
    pd.rect("blue", rec, 1)
    pd.arc("green", rec, -ang-view, -ang+view)
    for t in range(num):
        pd.line("green", (x, y), trans(x, y, r, ang+t/(num-1)-view), 2)
    
def check(arr, gr, pos, pd):
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
                arr[i][j] = 3
            pd.rect("graY", [p1, p2, fx, fy], 1)

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
qual = 100
view = 1/2
max_d = 100
x, y = 1.5*gr.x, 1.5*gr.y
sx, sy = 0, 0
run = True
grids[sx:sx+msz[1], sy:sy+msz[0]] = np.rot90(map)[::-1]
while run:
    #grids = nri(0, 3, siz)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
                
            if event.key == K_z:
                ang -= tau/16
            if event.key == K_x:
                ang += tau/16
                
    
    gr.draw(grids)
                  
    cone(pd, x, y, max_d, ang, view, qual)
    check(grids, gr, (x, y), pd)
    #pd.circ("red", (x, y), 10)
                                    
    pd.upd()
    pd.fill("black")