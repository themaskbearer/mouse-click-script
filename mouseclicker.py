    
import time
import pyautogui
from threading import Thread
from tkinter import *


class SimpleThread():

    def __init__(self):
        self._running = False
        self._thread = Thread(target=self.threadloop)

    def __del__(self):
        if hasattr(self, "m_thread"):
            self.stop()
        
    def start(self):
        if not hasattr(self, "m_thread"):
            self._thread = Thread(target=self.threadloop)

        self._running = True
        self._thread.start()
        
    def stop(self):
        if self._running:
            self._running = False
            self._thread.join()
            del self._thread
            
    def threadloop(self):
        pass

        
class MouseMoveThread(SimpleThread):
    CONST_TIMEOUT_COUNT = 10
    CONST_SLEEP_TIME = 0.25
    
    def threadloop(self):
        counter = self.CONST_TIMEOUT_COUNT

        while self._running:
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
    
    def threadloop(self):
        while self._running:
            location = pyautogui.position()
            locationstr = str(location)
            self.m_mouseLabelText.set(locationstr)
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
        
        self._click_thread = MouseMoveThread()
        
        self._mouse_label_text = StringVar()
        self._track_thread = MouseTrackingThread(self._mouse_label_text)
        
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        self._mouse_label = Label(self)
        self._mouse_label["textvariable"] = self._mouse_label_text
        self._mouse_label.grid(row=0, column=0, columnspan=2)
        self._track_thread.start()
        
        self._quit= QuitButton(self)
        self._quit["command"] = self.stop
        self._quit.grid(row=2, column=0)

        self._toggle_mouse = MouseToggleButton(self)
        self._toggle_mouse["command"] = self.toggle_mouse_clicks
        self._toggle_mouse.grid(row=2, column=1)
              
    def stop(self):
        self._track_thread.stop()
        self._click_thread.stop()
                       
        self.quit()   
        
    def toggle_mouse_clicks(self):
        if self._toggle_mouse.click():
            self._click_thread.start()
        else:
            self._click_thread.stop()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
