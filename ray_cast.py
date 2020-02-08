import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid, mou_pos
from uotp import graph
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
    pd.circ("white", (x, y), 10)
    #pd.rect("blue", rec, 2)
    pd.circ("blue", (x, y), r, 2)
    pts = []
    for t in range(num):
        po = trans(0, 0, r, ang-t/(num-1)*view*tau)
        #d = (po[0]+x, po[1]+y)
        #pd.line("green", (x, y), d, 2)
        pts.append((po[0]+x, po[1]+y))
    return pts

def intersection(p1, p2, p3, p4):
    x1, y1 = p1 
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    det = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    if det != 0:
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/det
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/det

        if 0 <= t <= 1 and 0 <= u <= 1:
            px = x1+t*(x2-x1)
            py = y1+t*(y2-y1)
            """ or this:
            px = x3+u*(x4-x3)
            py = y3+u*(y4-y3)
            """
            return [px, py]
        else:
            return [x4, y4]
    else:
        return False

def vecl(*arg):
    v = None
    if len(arg) == 1:
        e = arg[0]
        v = np.linalg.norm(e)
    elif len(arg) == 2:
        s, e = arg
        s1, s2 = s
        e1, e2 = e
        v = np.linalg.norm([e1-s1, e2-s2])
    return v

def min_p(arr, pos):
    min = float('Inf')
    m = None
    for j in range(len(arr)):
        i = arr[j]
        #if i == True:
            #return pos, True
        d = vecl(pos, i)
        if d < min:
            min = d
            m = arr[j]
    return m, min

def check(arr, gr, me, pd, rays):
    lines = []
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
            #pd.rect("graY", [p1, p2, fx, fy], 1)
            if arr[i][j] == 1:
                if arr[i+1][j] != 1:
                    lines += [[(p3, p4), (p3, p2)]]
                if arr[i-1][j] != 1:
                    lines += [[(p1, p2), (p1, p4)]]
                if arr[i][j+1] != 1:
                    lines += [[(p1, p4), (p3, p4)]]
                if arr[i][j-1] != 1:
                    lines += [[(p3, p2), (p1, p2)]]
    for lin in lines:
        pd.line("white", lin[0], lin[1], 4)
    dists = []
    for ray in rays:
        a = []
        for lin in lines:
            intr = intersection(lin[0], lin[1], pos, ray)
            if intr != False:
                #if intr == True:
                    #a.append(True)
                #else:
                a.append(intr)
            #elif intr == False:
                #a.append(None)
        intr, di = min_p(a, pos)
        if intr != None:
            pd.line("red", intr, pos)
            #pd.circ("lblue", intr, 5)
            dists.append(di)
            
    return dists

def transc(arr, max):
    cols = []
    for i in arr:
        if i == True:
            q = 255
        else:
            q = 255*i/max
        '''if q >= 127:
            cols.append(1)
        elif q < 127:
            cols.append(0)'''
        cols.append(q)
    return cols

class cha():
    def __init__(self, gr, x, y, view, ang, qual, r):
        self.view = view
        self.ang = ang
        self.qual = qual
        self.r = r
        self.gr = gr
        self.x, self.y = x*gr.x, y*gr.y
        
    def mov(self, x, y, u=1):
        if u == 0:
            self.x += x
            self.y += y
        elif u != 0:
            self.x += x*self.gr.x
            self.y += y*self.gr.y
            print(self.x)
        
    def pos(self, x, y, u=1):
        if u == 0:
            self.x = x
            self.y = y
        elif u != 0:
            self.x = x*self.gr.x
            self.y = y*self.gr.y

num = 2**5

pd = pyg_draw(2)
gr = Grid(pd, num, 0)
mou = mou_pos(pd)
gra = graph(pd, num)

wid, hei = pd.scr

qual = num#200
print(qual)
view = 1/8
r = gr.x*5
st = 0.25
rot_ang = tau/2**5

me = cha(gr, 5, 4, view, 0, qual, r)

siz = ((gr.row), (gr.col))
grids = np.full(siz, 0)

map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    ])
      
print(gr.colo(1))
      
msz = map.shape     
sx, sy = 0, 0
run =  True
grids[sx:sx+msz[1], sy:sy+msz[0]] = np.rot90(map)[::-1]
grd2 = np.full((gr.row, 1), 1)

#run = pd.pau()
while run:
    #grids = nri(0, 3, siz)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
                
            if event.key == K_z:
                me.ang -= rot_ang
            if event.key == K_x:
                me.ang += rot_ang
                
            if event.key == K_w:
                me.mov(0, -st)
                print(me.x, me.y)
            if event.key == K_s:
                me.mov(0, st)
            if event.key == K_a:
                me.mov(-st, 0)
            if event.key == K_d:
                me.mov(st, 0)
                
        if event.type != MOUSEBUTTONUP:
            #me.pos(*mou.mp(cent=0), u=0)
            #print(me.x, me.y)
            pass
    
    #gr.draw(grd2, yo=hei/2)
    #print(grd2)
                  
    rays = cone(pd, me)
    dists = check(grids, gr, me, pd, rays)
        
    darr, dists = gra.tran(dists, r, 2.5, 20)
        
    gra.draw(darr, dists)
    
    #me.ang -= 2*rot_ang
        
    #pd.pau()                     
    pd.upd()
    pd.fill("black")