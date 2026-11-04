"""
Daily Stock Report Automation Bot
Tools: PyAutoGUI, Chrome, Microsoft Excel
Website: Screener.in - Tata Motor Ltd
"""

import pyautogui
import pyperclip
import time
import re
import platform
import subprocess
from datetime import datetime
from pathlib import Path


# Configuration
URL = "https://www.screener.in/company/TMCV/consolidated/"
COMMENT = "Daily market check completed"

OUTPUT_DIR = Path(__file__).resolve().parent


def pause(seconds=2):
    time.sleep(seconds)


def hotkey(*keys):
    """Platform-appropriate keyboard shortcuts."""
    if platform.system() == "Darwin":
        keys = tuple(
            "command" if k == "ctrl" else k
            for k in keys
        )

    pyautogui.hotkey(*keys)


def open_app(app_name):

    system = platform.system()

    if system == "Windows":

        pyautogui.hotkey("win", "r")
        pause()

        pyautogui.write(app_name, interval=0.1)
        pyautogui.press("enter")

    elif system == "Darwin":

        pyautogui.hotkey("command", "space")
        pause()

        pyautogui.write(app_name, interval=0.1)
        pause()

        pyautogui.press("enter")

    else:

        command = (
            "google-chrome"
            if app_name.lower() == "chrome"
            else "libreoffice --calc"
        )

        subprocess.Popen(command.split())

    pause(5)


def fetch_stock_data():

    print("Opening Chrome...")

    open_app("Chrome")

    # Navigate to Screener website
    hotkey("ctrl", "l")

    pyperclip.copy(URL)
    #pyautogui.write(URL, interval=0.15)
    hotkey("ctrl", "v")

    pyautogui.press("enter")

    print("Loading Screener website...")

    pause(12)

    # Copy webpage information
    hotkey("ctrl", "a")
    hotkey("ctrl", "c")

    pause(2)

    page_text = pyperclip.paste()

    if not page_text:
        raise Exception("Unable to copy webpage information.")

    # Extract stock price
    patterns = [
        r"Current Price\s*₹?\s*([\d,]+(?:\.\d+)?)",
        r"₹\s*([\d,]+(?:\.\d+)?)",
        r"Rs\.?\s*([\d,]+(?:\.\d+)?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            page_text,
            re.IGNORECASE
        )

        if match:

            price = match.group(1)

            return f"Tata Motor Ltd : ₹{price}"

    raise Exception("Stock price not found on webpage.")


def open_excel():

    print("Opening Excel...")

    if platform.system() == "Windows":

        open_app("Excel")

    elif platform.system() == "Darwin":

        open_app("Microsoft Excel")

    else:

        open_app("LibreOffice Calc")

    # Create new workbook
    hotkey("ctrl", "n")

    pause(3)


def create_report(stock_data):

    now = datetime.now()

    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    today = now.strftime("%Y-%m-%d")

    excel_file = OUTPUT_DIR / f"daily_report_{today}.xlsx"

    screenshot_file = OUTPUT_DIR / f"daily_report_{today}.png"

    print("Creating Excel report...")

    open_excel()

    # Prepare Excel data
    report_data = (
        "Date & Time\tShare Price\tComment\n"
        f"{date_time}\t{stock_data}\t{COMMENT}"
    )

    # Enter data into Excel
    pyperclip.copy(report_data)

    hotkey("ctrl", "v")

    pause(3)

    # Save Excel file
    print("Saving Excel file...")

    if platform.system() == "Darwin":

        hotkey("command", "shift", "s")

    else:

        pyautogui.press("f12")

    pause(3)

    # Enter filename
    pyperclip.copy(str(excel_file))

    hotkey("ctrl", "v")

    pyautogui.press("enter")

    pause(4)

    # Confirm possible dialog
    pyautogui.press("enter")

    pause(2)

    # Take screenshot
    print("Taking screenshot...")

    pyautogui.screenshot().save(str(screenshot_file))

    print("\nReport successfully created!")

    print("Excel File:", excel_file)

    print("Screenshot:", screenshot_file)


def close_applications():

    print("\nClosing Chrome and Excel...")

    pause(2)

    # Close Excel first
    hotkey("alt", "f4")

    pause(3)

    # Switch to Chrome
    hotkey("alt", "tab")

    pause(1)

    # Close Chrome
    hotkey("alt", "f4")

    pause(2)

    print("Chrome and Excel closed successfully!")


def main():

    pyautogui.FAILSAFE = True

    pyautogui.PAUSE = 0.5

    try:

        print("================================")
        print(" DAILY STOCK REPORT AUTOMATION ")
        print("================================")

        # Step 1: Fetch stock data
        stock_data = fetch_stock_data()

        print("Share Price:", stock_data)

        # Step 2: Create Excel report
        create_report(stock_data)

        # Step 3: Close applications
        close_applications()

        print("\nAutomation completed successfully!")

    except Exception as error:

        print("\nError occurred:", error)


if __name__ == "__main__":

    main()
