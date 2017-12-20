
import time
from threading import Thread
import pyautogui
from tkinter import *

 
 
class Application(Frame):
    CONST_TIMEOUT_COUNT = 5
    CONST_SLEEP_TIME = 0.25
    CONST_MOUSE_TRACK_REFRESH_sec = 0.1

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.m_mouseLabel = Label(self)
        self.m_mouseLabelText = StringVar()
        self.m_mouseLabelText.set("Placeholder")
        self.m_mouseLabel["textvariable"] = self.m_mouseLabelText
        self.m_mouseLabel.grid(row=0, column=0, columnspan=2)
        self.startMouseTracking()
        
        self.m_quit= Button(self)
        self.m_quit["text"] = "Quit"
        self.m_quit["fg"]   = "white"
        self.m_quit["bg"] = "red"
        self.m_quit["command"] =  self.stop
        self.m_quit.grid(row=2, column=0)

        self.m_startMouse = Button(self)
        self.m_startMouse["text"] = "Start Mouse"
        self.m_startMouse["command"] = self.startClicks
        self.m_startMouse.grid(row=2, column=1)
              
    def startMouseTracking(self):
        if not hasattr(self, 'm_clickThread'):
            self.m_trackThread = Thread(target = self.trackMouse)
            self.m_running = True
            self.m_trackThread.start()
        else:
            print("ERROR: Mouse tracking is already running")
            
    def trackMouse(self):
        while self.m_running == True:
            location = pyautogui.position()
            locationStr = str(location)
            self.m_mouseLabelText.set(locationStr)
            time.sleep(self.CONST_MOUSE_TRACK_REFRESH_sec)
              
    def stop(self):
        self.m_running = False
        if hasattr(self, 'm_clickThread'):
            self.m_clickThread.join()
        if hasattr(self, 'm_trackThread'):
            self.m_trackThread.join()
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


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()