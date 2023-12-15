import pymem
import pyautogui
import pynput
import time
from pynput.mouse import Button

class Vector:
    def __init__(self, process, base_address, blink_address, blinksub = lambda x: x):
        self.process = process
        self.address = base_address 
        self.blink_address = blink_address
        self._x = 0.0
        self._y = 0.0
        self._blink = True
        self.active = False
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
    
def blinksub():
    if 0.95 < vector.y < 1.2 and  0.45<vector.x < 0.55:
        vector.active = not vector.active
        print("active") if vector.active else print("inactive")
    if vector.active:
        print("blink")
        if vector.x > 0.8:
            pyautogui.press('right')
        elif vector.x < 0.2:
            pyautogui.press('left')
    time.sleep(0.1)
    
def on_click(x, y, button, pressed):
    if button == Button.x2:
        print("Mouse button 5 is clicked")
    if button == Button.x1:
        print("Mouse button 4 is clicked")

process = pymem.Pymem("TobiiGhost.exe")
vector = Vector(process, 0x04E93314,0x1D0C75E4, blinksub)
screen_width, screen_height = pyautogui.size()
listener = pynput.mouse.Listener(on_click=on_click)
listener.start()
pyautogui.FAILSAFE = False

while True:
    vector.update()
    if vector.active:
        print(vector.blink, vector.x, vector.y)
        if vector.y > 0.7:
            pyautogui.vscroll(int(-500 * (vector.y - 0.7)))
        elif vector.y < 0.2:
            pyautogui.vscroll(int(500 * (0.2 - vector.y)))
        else:
            time.sleep(0.01)
    else:
        time.sleep(0.1)


    
