import pyautogui
import time
from datetime import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5


print("Step 1:Open the chrome browser...")
time.sleep(2)

pyautogui.hotkey('win', 'r', interval=0.1)
time.sleep(1)
pyautogui.write('chrome', interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)

print("Step 2:Go to the website...")
pyautogui.hotkey('ctrl', 't', interval=0.1)
time.sleep(1)
pyautogui.write('https://www.accuweather.com/en/in/bengaluru/204108/weather-forecast/204108', interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(5)

print("Step 3: Copy the full data of the website...")
pyautogui.hotkey('ctrl', 'a', interval=0.1)
time.sleep(1)
pyautogui.hotkey('ctrl', 'c', interval=0.1)
time.sleep(1)  

print("Step 4: Open the text editor and paste the data...")
pyautogui.hotkey('win', 'r', interval=0.1)
time.sleep(1)
pyautogui.write('notepad', interval=0.15)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)
pyautogui.hotkey('ctrl', 'n', interval=0.1)
time.sleep(3)
pyautogui.hotkey('ctrl', 'v', interval=0.1)
time.sleep(2)