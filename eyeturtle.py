import pymem
import pyautogui
import math
import time
LATP = 0

class v:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def transform(p, mx = v(-1,-1),my=v(1,1)):
    px =  ((p.x - mx.x) / (my.x - mx.x)) * 600 - 300
    py =  ((p.y - mx.y) / (my.y - mx.y)) * 600 - 300
    return v(px,py)
        
def turtleForMePlease(t, p,):
    global LATP
    atp = math.degrees(math.atan2((p.y - t.y), (p.x - t.x)))
    dtp = math.sqrt(((p.x - t.x) ** 2) + ((p.y - t.y) ** 2))
    if ((((atp - LATP) % 360) + 360) % 360) > 180:
        t.right(360 - (((atp - LATP) % 360) + 360) % 360)
    else:
        t.left((((atp - LATP) % 360) + 360) % 360)
    t.forward(dtp)
    LATP = atp

class Vector:
    def __init__(self, process, base_address, blink_address, blinksub = lambda x: x):
        self.process = process
        self.address = base_address 
        self.blink_address = blink_address
        self._x = 0.0
        self._y = 0.0
        self._blink = True
        self.active = True
        self.blinksub = blinksub
        self._ox = []
        self._oy = []

    def update(self):
        blink = self.process.read_int(self.blink_address) != 1
        if blink == True and self._blink == False:
            self._x = self._ox[0]
            self._y = self._oy[0]
            self.blinksub()
        self._blink = blink
        self._x = self.process.read_float(self.address)
        self._y = self.process.read_float(self.address + 4)
        self._ox.append(self._x)
        self._oy.append(self._y)
        self._ox = self._ox[-2:]
        self._oy = self._oy[-2:]

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def blink(self):
        return self._blink
    
def calibrate(vector,vc):
    turtleForMePlease(turtle,vc)
    time.sleep(0.5)
    vector.update()
    return v(vector.x,vector.y)
    
def blinksub():
    check()
    exit()

import random

def snap(t, p, d):
    distance = math.sqrt(((p.x - t.x) ** 2) + ((p.y - t.y) ** 2))
    if distance < d:
        turtleForMePlease(turtle, v(p.x + random.uniform(-5, 5), p.y + random.uniform(-5, 5)))
        return True

process = pymem.Pymem("TobiiGhost.exe")

vector = Vector(process, 0x04E93314,0x1D0C75E4, blinksub)
screen_width, screen_height = pyautogui.size()

from turtlelab3x import turtle,home,shop,check
vy = calibrate(vector,v(300,300))
vx = calibrate(vector,v(-300,-300))

while True:
    vector.update()
    snap(transform(vector,vx,vy),shop,30) or\
    snap(transform(vector,vx,vy),home,30) or\
    turtleForMePlease(turtle, transform(vector,vx,vy))






    
