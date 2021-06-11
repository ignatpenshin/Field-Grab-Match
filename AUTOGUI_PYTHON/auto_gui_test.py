import pyautogui
import time
import keyboard
import win32api, win32con
import getpass
import os

os.chdir(getpass.getuser())

def click(x, y, right=False):
    if right == False:
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    else:
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        
x = 0
while True:
    time.sleep(2)
    if pyautogui.locateOnScreen("name.png", confidence=0.9) != None:
        print("I can see it")
        time.sleep(5)
        click(75, 140)
        time.sleep(3)
        keyboard.send('ctrl+a')
        time.sleep(20)
        click(75, 140, right=True)
        
        while True:
            if pyautogui.locateOnScreen("merge.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('merge.png')
                time.sleep(5)
                click(x,y)
                break
              
        while True:
            if pyautogui.locateOnScreen("file.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('file.png')
                time.sleep(5)
                click(x,y)
                break
        while True:
            if pyautogui.locateOnScreen("export.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('export.png')
                time.sleep(5)
                click(x,y)
                break
        while True:
            if pyautogui.locateOnScreen("library.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('library.png')
                time.sleep(5)
                click(x,y)
                break
        while True:
            if pyautogui.locateOnScreen("docs.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('docs.png')
                time.sleep(5)
                click(x,y)
                keyboard.press('enter')
                time.sleep(5)
                break
        while True:
            if pyautogui.locateOnScreen("TRACKS.png", confidence=0.7) != None:
                x, y = pyautogui.locateCenterOnScreen('TRACKS.png')
                time.sleep(5)
                click(x,y)
                time.sleep(0.5)
                keyboard.press('enter')
                break 
        while True:
            if pyautogui.locateOnScreen("GPS.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('GPS.png')
                time.sleep(1)
                click(x,y)
                keyboard.write('final_merged')
                time.sleep(5)
                keyboard.press('enter')
                time.sleep(5)
                keyboard.press('enter')
                time.sleep(5)
                break
        while True:
            if pyautogui.locateOnScreen("exit.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('exit.png')
                time.sleep(4)
                click(x,y)
                time.sleep(4)
                break         
        while True:
            if pyautogui.locateOnScreen("NO.png", confidence=0.9) != None:
                x, y = pyautogui.locateCenterOnScreen('NO.png')
                time.sleep(1)
                click(x,y)
                time.sleep(1)
                x = 1
                click(x,y)
                break
        if x == 1:
            break
print("final")
