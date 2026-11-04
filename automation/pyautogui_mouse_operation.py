import pyautogui
import time

time.sleep(3)
#Mouse operations
# pyautogui.moveTo(100, 100, duration=1)

#pyautogui.click(100, 100)
# pyautogui.rightClick(100, 100) 
#pyautogui.leftClick(100, 100)  # Left-click at position (100, 100)

#pyautogui.doubleClick(100, 100)  # Double-click at position (100, 100)

# pyautogui.dragTo(200, 200, duration=1)  # Drag the mouse to position (200, 200) over 1 second


pyautogui.scroll(500)  # Scroll up 500 units
time.sleep(1)
pyautogui.scroll(-500)  # Scroll down 500 units