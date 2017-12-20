
import time
from threading import Thread
import pyautogui
from tkinter import *

 
 
class Application(Frame):
    CONST_TIMEOUT_COUNT = 5
    CONST_SLEEP_TIME = 0.25

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.m_quit= Button(self)
        self.m_quit["text"] = "Quit"
        self.m_quit["fg"]   = "white"
        self.m_quit["bg"] = "red"
        self.m_quit["command"] =  self.stop
        self.m_quit.pack({"side": "left"})

        self.m_startMouse = Button(self)
        self.m_startMouse["text"] = "Start Mouse"
        self.m_startMouse["command"] = self.startClicks
        self.m_startMouse.pack({"side": "left"})
        
        self.m_getMouse = Button(self)
        self.m_getMouse["text"] = "Get Mouse Position"
        self.m_getMouse["command"] = self.getMousePosition
        self.m_getMouse.pack({"side": "left"})
        
    def stop(self):
        self.m_running = False
        if hasattr(self, 'm_clickThread'):
            self.m_clickThread.join()
        self.quit()   
        
    def startClicks(self):
        if not hasattr(self, 'm_clickThread'):
            self.m_clickThread = Thread(target = self.clickMouse)
            self.m_running = True
            self.m_clickThread.start()
        else:
            pyautogui.alert("Mouse is already running")

    def clickMouse(self):
        counter = self.CONST_TIMEOUT_COUNT
        while self.m_running == True:
            
            if counter < self.CONST_TIMEOUT_COUNT:
                counter += self.CONST_SLEEP_TIME
                time.sleep(self.CONST_SLEEP_TIME)
            else:        
                pyautogui.click(100, 200)
                time.sleep(1)
                pyautogui.click(200, 200)
                
                counter = 0
        
    def getMousePosition(self):
        print('Press Ctrl-C to quit.')
        try:
            while True:
                x, y = pyautogui.position()
                positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                print(positionStr, end='')
                print('\b' * len(positionStr), end='', flush=True)
        except KeyboardInterrupt:
            print('\n')


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()