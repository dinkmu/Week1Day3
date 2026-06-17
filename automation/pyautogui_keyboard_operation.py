import pyautogui
import time
import pyscreeze
'''
pyautogui.typewrite("Hello, World!", interval=0.1) 

#hot keys
pyautogui.hotkey('cmd', 'c')  # Simulate pressing Ctrl+C`
pyautogui.hotkey('cmd', 'v')  # Simulate pressing Ctrl+V
pyautogui.hotkey('cmd', 'a')  # Simulate pressing Ctrl+A
pyautogui.hotkey('cmd', 's')  # Simulate pressing Ctrl+

#pressing special keys
pyautogui.press('enter')  # Simulate pressing the Enter key
pyautogui.press('tab')    # Simulate pressing the Tab key
pyautogui.press('esc')    # Simulate pressing the Escape key
'''
#holding down keys
#pyautogui.keyDown('shift')  # Hold down the Shift key
#pyautogui.typewrite("this is uppercase")  # Type while holding Shift (will be uppercase)
#pyautogui.keyUp('shift')    # Release the Shift key


screenshot = pyautogui.screenshot()
screenshot.save("final.png")