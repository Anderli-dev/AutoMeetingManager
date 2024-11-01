import pyautogui
import schedule
import time
from datetime import datetime
import os

from get_filenames import get_filenames
from make_audio import make_audio
from transcription import audio_transcription


def handle_recording():
    # Switch to the OBS window for screen recording
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)

    # Move the mouse to the recording start button in OBS and click to start recording
    pyautogui.moveTo(1650, 825)
    pyautogui.click(button='left')
    time.sleep(0.5)

    # Switch back to the previous window
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)


# Function to handle mouse manipulations for joining a conversation
def join_conversation():
    # Move mouse to the "Join" button of the conversation application and click it
    pyautogui.moveTo(700, 590)
    pyautogui.click(button='left')
    time.sleep(2.5)

    # Move mouse to the "Video" button and enable video
    pyautogui.moveTo(765, 740)
    pyautogui.click(button='left')
    time.sleep(0.5)

    # Move mouse to the "Mic" button to enable microphone
    pyautogui.moveTo(685, 740)
    pyautogui.click(button='left')
    time.sleep(0.5)

    # Switch to the previous tab using keyboard shortcut to adjust focus
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    time.sleep(0.5)

    # Close the current tab if it's no longer needed
    pyautogui.hotkey('ctrl', 'f4')
    time.sleep(0.5)

    # Move mouse to another "Join" button if present and click it to fully join the conversation
    pyautogui.moveTo(1340, 635)
    pyautogui.click(button='left')
    time.sleep(0.5)


# Function to quit the conversation
def quit_conversation():
    # Close the current tab to exit the conversation
    pyautogui.hotkey('ctrl', 'f4')
    time.sleep(0.5)


def handle_meeting(start_time: str, end_time: str):
    # Split start and end times into hours and minutes
    split_start_time = start_time.split(":")
    split_end_time = end_time.split(":")

    # Schedule the recording start at the specified start time
    schedule.every().day.at(start_time).do(handle_recording)

    # Schedule joining the conversation 5 minutes after the start time
    schedule.every().day.at(split_start_time[0] + ":" + str(int(split_start_time[1]) + 5)).do(join_conversation)

    # Schedule quitting the conversation at the specified end time
    schedule.every().day.at(end_time).do(quit_conversation)

    # Schedule stopping the recording 5 minutes after the end time
    schedule.every().day.at(split_end_time[0] + ":" + str(int(split_end_time[1]) + 5)).do(handle_recording)


# Schedule the join and quit functions at specific times
handle_meeting("09:45", "11:20")

# Define the end time for the program (in HH:MM format)
# !!!IMPORTANT!! Time is last meeting ending time + 10 min
end_time_str = "13:30"
end_meeting_time = datetime.strptime(end_time_str, "%H:%M").time()

# Main loop to execute scheduled tasks and check for end time
try:
    while True:
        # Get the current time
        current_time = datetime.now().time()

        # Stop the program if the current time reaches the end time
        if current_time >= end_meeting_time:
            print("Meetings have ended. Time to make transcription")
            break

        # Run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

    # Retrieve the filenames of today's recorded videos
    today_videos_filenames = get_filenames()

    # Convert recorded videos to audio files
    make_audio(today_videos_filenames)

    # Perform audio transcription on the recorded audio files
    audio_transcription(today_videos_filenames)

    # Wait for 5 minutes, then shut down the computer
    time.sleep(60 * 5)
    os.system("shutdown /s /t 1")

# Catch manual interruptions (Ctrl+C)
except KeyboardInterrupt:
    print("\nProgram terminated.")
