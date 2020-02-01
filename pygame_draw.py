import pygame
from pygame.locals import *

class pyg_draw():
    def __init__(self, device, rev=0, alpha=0, wind_name="pygame window"):
        pygame.init()

        if device == 1:
            self.scr = (1080, 2340)
        if device == 2:
            n = 87
            self.scr = (17*(n+1), 9*n)

        if rev == 1:
            self.scr = self.scr[::-1]

        self.device = device

        flags = RESIZABLE #FULLSCREEN |  | SRCALPHA 
        self.wind = pygame.display.set_mode(self.scr, flags)
        #self.scr = self.wind.get_size()
        self.sur = pygame.Surface(self.scr, SRCALPHA)
        
        pygame.display.set_caption(wind_name)

        self.colors = {
            "red":(255, 0, 0),
            "green":(0, 255, 0),
            "blue":(0, 0, 255),
            "white":(255, 255, 255),
            "black":(0, 0, 0),
            "gray":(127, 127, 127),
            }

        self.fonts = []

    def col(self, name):
        if isinstance(name, str) is True:
            color = self.colors
            return color.get(name.lower())
        else:
            return name

    def cen(self, a=2, b=2):
        return (self.scr[0]/a, self.scr[1]/b)
        
    def circ(self, col, pos, rad=1, wid=0):
        if pos[0] != None:
            col = self.col(col)
            if wid > rad:
                rad = wid
            try:
                pygame.draw.circle(self.sur, col, (int(pos[0]), int(pos[1])), int(rad), (wid))
            except Exception: pass
        
    def line(self, col, pos1, pos2, wid=1, aa=0, blend=0):
        if pos1[0] != None and pos2[0] != None:
            col = self.col(col)
            try:
                if aa == 0:
                    pygame.draw.line(self.sur, col, pos1, pos2, wid)
                else:
                    pygame.draw.aaline(self.sur, col, pos1, pos2, blend)
            except Exception: pass

    def poly(self, col, pos_s):
        col = self.col(col)
        try:
            pygame.draw.polygon(self.sur, col, pos_s, 0)
        except Exception: pass
       
    def rect(self, col, arr, wid=0):
        col = self.col(col)
        try:
            pygame.draw.rect(self.sur, col, arr, wid)
        except Exception: pass
        
    def elip(self, col, rec, wid=1):
        col = self.col(col)
        try:
            pygame.draw.ellipse(self.sur, col, rec, wid)
        except Exception: pass
    
    def arc(self, col, rec, sa, ea, wid=1):
        col = self.col(col)
        try:
            pygame.draw.arc(self.sur, col, rec, sa, ea, wid)
        except Exception: pass

    def font_init(self, font_size, num_symol, col, rect_wid=1, txt_font="arial", rect=1):
        col = self.col(col)
        font = pygame.font.SysFont(txt_font, font_size)
        if rect == 1:
            siz = (font_size*0.65*num_symol, font_size*1.1)
            sur = pygame.Surface(siz)
            pygame.draw.rect(sur, col, (0, 0, *siz), rect_wid)
            black = sur.copy()
        else:
            sur, black = None, None
        self.fonts.append([font, col, sur, black])

    def text(self, num, txt, point):
        val = self.fonts[num]
        font = val[0]
        text = font.render(str(txt), 1, val[1])
        if val[2] != None:
            val[2].blit(val[3], (0, 0))
            val[2].blit(text, (5, 0))
            self.sur.blit(val[2], point)
        else:
            self.sur.blit(text, point)

    def blit(self, sur2, pos):
        self.sur.blit(sur2, pos)
        
    def fill(self, col):
        if isinstance(col, str) is True:
            col = self.col(col)
        self.sur.fill(col)
        self.wind.fill(col)
        
    def upd(self):
        self.wind.blit(self.sur, (0, 0))
        pygame.display.flip()
        
    def ret(self):
        return self.sur

    def pau(self):
        while 1:
            event = pygame.event.wait()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
                
class Grid():
    def __init__(self, pd, num, off=0.1):
        self.pd = pd
        w, h = pd.scr
        if pd.device == 1:
            row = 6*num
            col = 13*num
        else:
            row = 17*num
            col = 9*num
        self.row, self.col = row, col 
        ax, ay = w/row, h/col
        margx, margy = ax*off, ay*off
        self.mx, self.my = margx, margy
        self.x, self.y = ax, ay
        self.colors = {
            3:"red",
            4:"green",
            5:"blue",
            1:"white",
            0:"black",
            2:"gray",
            }
        
    def colo(self, color):
        return self.colors.get(color)
        
    def draw(self, grid):
        row, col = self.row, self.col
        x, y = self.x, self.y
        mx, my = self.mx, self.my
        fx, fy = x-mx, y-my
        for i in range(row):
            for j in range(col):
                color = self.colo(grid[i][j])
                p1 = x*i+mx/2
                p2 = y*j+my/2
                self.pd.rect(color, [p1, p2, fx, fy])
                    