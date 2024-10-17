import pyautogui
import schedule
import time
from datetime import datetime
import os


# Function to handle mouse manipulations for joining a conversation
def join_conversation():
    # Move mouse to the "Join" button and click it
    pyautogui.moveTo(700, 590)
    pyautogui.click(button='left')
    time.sleep(2.5)

    # Move mouse to the "Video" button and click it
    pyautogui.moveTo(765, 740)
    pyautogui.click(button='left')
    time.sleep(0.5)

    # Move mouse to the "Mic" button and click it
    pyautogui.moveTo(685, 740)
    pyautogui.click(button='left')
    time.sleep(0.5)

    # Switch to the previous tab using keyboard shortcut
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    time.sleep(0.5)

    # Close the current tab using keyboard shortcut
    pyautogui.hotkey('ctrl', 'f4')
    time.sleep(0.5)

    # Move mouse to another "Join" button and click it
    pyautogui.moveTo(1340, 605)
    pyautogui.click(button='left')
    time.sleep(0.5)


# Function to quit the conversation
def quit_conversation():
    # Close the current tab using keyboard shortcut
    pyautogui.hotkey('ctrl', 'f4')
    time.sleep(0.5)


# Schedule the join and quit functions at specific times
schedule.every().day.at("09:45").do(join_conversation)
schedule.every().day.at("11:20").do(quit_conversation)

# Define the end time for the program (in HH:MM format)
end_time_str = "11:30"
end_time = datetime.strptime(end_time_str, "%H:%M").time()

# Main loop to execute scheduled tasks and check for end time
try:
    while True:
        # Get the current time
        current_time = datetime.now().time()

        # Stop the program if the current time reaches the end time
        if current_time >= end_time:
            print("Program runtime has ended. Shutting down.")
            os.system("shutdown /s /t 1")
            break

        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

# Catch manual interruptions (Ctrl+C)
except KeyboardInterrupt:
    print("\nProgram terminated.")
