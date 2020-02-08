import pygame
from pygame.locals import *
from pygame_draw import pyg_draw, Grid, mou_pos
from numpy.random import randint as nri
import numpy as np

class graph():
    def __init__(self, pd, num):
        w, h = pd.scr
        self.pd = pd
        self.w = w
        self.h = h
        self.bw = w/num
        self.bh = h/2
        
    def draw(self, arr, arr2, xo=0, yo=0):
        bw, bh = self.bw, self.bh
        h, w = self.h, self.h
        pd = self.pd
        for i in range(len(arr)):
            for j in range(1):
                k = arr[i]
                p3 = bw
                p4 = arr2[i]
                p1 = p3*i  +xo
                p2 = p4*j+h/2  +yo
                pd.rect((k, k, k), [p1, p2, p3, p4])
                pd.rect((k, k, k), [p1, p2, p3, -p4])
                
    def tran(self, arr, max, mul=1, m2=1):
        b = []
        for i in range(len(arr)):
            if arr[i] >= max-1:
                arr[i] = 0
            else:
                arr[i] = 1/arr[i]*mul*max
            b.append(255*arr[i]/max)
            arr[i] *= m2
        return b, arr
        
if __name__ == "__main__":
    num = 100
    pd = pyg_draw(1, rev=0)
    gr = graph(pd, num)
    
    bw, bh = gr.bw, gr.bh
    arr = np.arange(0, 255, 255/num)
    #arr = nri(100, 255, num)
    arr2 = np.arange(0, bh, bh/num)
    #arr2 = nri(0, bh, num)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                if event.key == K_SPACE:
                    pd.pau()
       
        arr2 = nri(0, bh, num)
        arr, arr2 = gr.tran(arr2, bh)
                                
        gr.draw(arr, arr2)
                
        pd.upd()
        pd.fill("black")