    
import time
import pyautogui
from threading import Thread
from tkinter import *


class SimpleThread():

    def __init__(self):
        self.m_running = False

    def __del__(self):
        if hasattr(self, "m_thread"):
            self.stop()
        
    def start(self):
        if not hasattr(self, "m_thread"):
            self.m_thread = Thread(target = self.threadLoop)
            self.m_running = True
            self.m_thread.start()
        
    def stop(self):
        if self.m_running == True:
            self.m_running = False
            self.m_thread.join()
            del self.m_thread
            
    def threadLoop(self):
        pass

        
class MouseMoveThread(SimpleThread):
    CONST_TIMEOUT_COUNT = 10
    CONST_SLEEP_TIME = 0.25
    
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
 
 
class MouseTrackingThread(SimpleThread):
    CONST_MOUSE_TRACK_REFRESH_sec = 0.1
    
    def __init__(self, positionStr):
        SimpleThread.__init__(self)
        self.m_mouseLabelText = positionStr
    
    def threadLoop(self):
        while self.m_running == True:
            location = pyautogui.position()
            locationStr = str(location)
            self.m_mouseLabelText.set(locationStr)
            time.sleep(self.CONST_MOUSE_TRACK_REFRESH_sec)
    

class QuitButton(Button):
    
    def __init__(self, frame):
        Button.__init__(self, frame)
        
        self["text"] = "Quit"
        self["fg"] = "white"
        self["bg"] = "red"


class MouseToggleButton(Button):

    def __init__(self, frame):
        Button.__init__(self, frame)
        
        self["text"] = "Start Mouse"
        
    def click(self):
        if self["text"] == "Start Mouse":
            self["text"] = "Stop Mouse"
            return True
        else:
            self["text"] = "Start Mouse"
            return False

    
class Application(Frame):
    CONST_MOUSE_TRACK_REFRESH_sec = 0.1

    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.m_clickThread = MouseMoveThread()
        
        self.m_mouseLabelText = StringVar()
        self.m_trackThread = MouseTrackingThread(self.m_mouseLabelText)
        
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        self.m_mouseLabel = Label(self)
        self.m_mouseLabel["textvariable"] = self.m_mouseLabelText
        self.m_mouseLabel.grid(row=0, column=0, columnspan=2)
        self.m_trackThread.start()
        
        self.m_quit= QuitButton(self)
        self.m_quit["command"] =  self.stop
        self.m_quit.grid(row=2, column=0)

        self.m_toggleMouse = MouseToggleButton(self)
        self.m_toggleMouse["command"] = self.toggleMouseClicks
        self.m_toggleMouse.grid(row=2, column=1)
              
    def stop(self):
        self.m_trackThread.stop()
        self.m_clickThread.stop()        
                       
        self.quit()   
        
    def toggleMouseClicks(self):
        if self.m_toggleMouse.click():
            self.m_clickThread.start()
        else:
            self.m_clickThread.stop()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()