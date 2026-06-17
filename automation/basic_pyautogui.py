import pyautogui
import time

print("move your mouse to the button you want to click in 5 seconds...")
time.sleep(5)

x,y = pyautogui.position()
print(f"clicking at position: {x}, {y}")
#pyautogui.click(x, y)