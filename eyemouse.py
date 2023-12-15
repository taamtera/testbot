import pymem
import pyautogui
import time
import speech_recognition as sr

LATP = 0

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
        pyautogui.moveTo(int(vector.x * screen_width), int(vector.y * screen_height))
        pyautogui.click()
        print("click")
    time.sleep(0.1)


def start_listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source,phrase_time_limit=6)

    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
        pyautogui.typewrite(text)
        pyautogui.press('enter')
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

process = pymem.Pymem("TobiiGhost.exe")
vector = Vector(process, 0x04E93314,0x1D0C75E4, blinksub)
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False
bs = 0

while True:
    vector.update()
    if vector.active:
        print(vector.blink, vector.x, vector.y)
        pyautogui.moveTo(int(vector.x * screen_width), int(vector.y * screen_height))
        if vector.blink:
            bs += 1
            if bs == 5:
                start_listening()
                bs = 0
        else:
            bs = 0
    else:
        time.sleep(0.01)







