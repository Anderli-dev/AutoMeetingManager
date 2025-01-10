import time
import pyautogui
import schedule
from datetime import datetime, timedelta


class MeetingHandler:
    def __init__(self):
        # List to store meeting end times
        self.meetings_end_time = []
        # Initialize the scheduler
        self.schedule = schedule

    def get_latest_time(self):
        # Returns the latest meeting end time
        return max(self.meetings_end_time)

    # Function to handle mouse manipulations for joining a conversation
    def join_conversation(self):
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
    def quit_conversation(self):
        # Close the current tab to exit the conversation
        pyautogui.hotkey('ctrl', 'f4')
        time.sleep(0.5)

    def handle_recording(self):
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

    def create_meeting_session(self, start_time: str, end_time: str):
        # Add the meeting end time to the list of end times
        self.meetings_end_time.append(
            datetime.strptime(end_time, "%H:%M")
        )

        # Schedule the recording to start at the specified start time
        self.schedule.every().day.at(start_time).do(self.handle_recording)

        # Schedule joining the conversation 5 minutes after the start time
        self.schedule.every().day.at(
            (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        ).do(self.join_conversation)

        # Schedule quitting the conversation at the specified end time
        self.schedule.every().day.at(end_time).do(self.quit_conversation)

        # Schedule stopping the recording 5 minutes after the end time
        self.schedule.every().day.at(
            (datetime.strptime(end_time, "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        ).do(self.handle_recording)
