
import pyautogui

location = pyautogui.position()

pyautogui.alert('The mouse is at ' + str(location))
