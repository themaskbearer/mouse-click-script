    
import time
import pyautogui
from threading import Thread
from tkinter import *



class MouseMoveThread():
    CONST_TIMEOUT_COUNT = 10
    CONST_SLEEP_TIME = 0.25
    
    def __init__(self):
        self.m_thread = Thread(target = self.threadLoop)
        self.m_running = False
    
    def __del__(self):
        if self.m_running == True:
            self.stop()
    
    def start(self):
        self.m_running = True
        self.m_thread.start()
        
    def stop(self):
        if self.m_running == True:
            self.m_running = False
            self.m_thread.join()
        
    def threadLoop(self):
        counter = self.CONST_TIMEOUT_COUNT
        while self.m_running == True:
            
            if counter < self.CONST_TIMEOUT_COUNT:
                counter += self.CONST_SLEEP_TIME
                time.sleep(self.CONST_SLEEP_TIME)
            else:        
                pyautogui.click(16, 156)
                time.sleep(1)
                pyautogui.click(163, 154)
                
                counter = 0
 
class Application(Frame):
    
    CONST_MOUSE_TRACK_REFRESH_sec = 0.1

    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.m_clickThread = MouseMoveThread()
        
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

        self.m_toggleMouse = Button(self)
        self.m_toggleMouse["text"] = "Start Mouse"
        self.m_toggleMouse["command"] = self.startClicks
        self.m_toggleMouse.grid(row=2, column=1)
              
    def startMouseTracking(self):
        if not hasattr(self, 'm_trackThread'):
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
            self.m_clickThread.stop()
        if hasattr(self, 'm_trackThread'):
            self.m_trackThread.join()
                       
        self.quit()   
        
    def startClicks(self):
        if self.m_toggleMouse["text"] == "Start Mouse":
            self.m_clickThread.start()
            self.m_toggleMouse["text"] = "Stop Mouse"
        else:
            self.m_clickThread.stop()
            self.m_toggleMouse["text"] = "Start Mouse"



root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()