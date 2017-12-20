
import time
from threading import Thread
import pyautogui
from tkinter import *

 
 
class Application(Frame):
    def startClicks(self):
        if not hasattr(self, 'clickThread'):
            self.clickThread = Thread(target = self.clickMouse)
            self.running = True
            self.clickThread.start()
        else:
            pyautogui.alert("Mouse is already running")

    def clickMouse(self):
        while self.running == True:
            pyautogui.moveTo(100, 200)
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(200, 200)
            pyautogui.click()
            time.sleep(5)
        
    def stop(self):
        self.running = False
        if hasattr(self, 'clickThread'):
            self.clickThread.join()
        self.quit()
        
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"]   = "white"
        self.QUIT["bg"] = "red"
        self.QUIT["command"] =  self.stop

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Start Mouse"
        self.hi_there["command"] = self.startClicks

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()