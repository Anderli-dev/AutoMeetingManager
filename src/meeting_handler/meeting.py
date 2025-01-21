import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import pyautogui
import schedule

from src.realtime_recognizer.RealtimeSpeechRecognizer import RealtimeSpeechRecognizer
from src.conversation.conversation import Conversation


async def async_wrapper(func):
    """
    Wraps a synchronous function to execute it in an asynchronous loop.
    Utilizes a thread pool to ensure compatibility with asyncio.
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as thread_executor:
        return await loop.run_in_executor(thread_executor, func)


def create_async_task(task):
    """
    Creates and runs an asynchronous task for non-blocking execution.
    """
    asyncio.create_task(async_wrapper(task))


class MeetingHandler:
    def __init__(self):
        # List to store meeting end times
        self.meetings_end_time = []
        # Initialize the scheduler
        self.schedule = schedule.Scheduler()
        self.recognizer = RealtimeSpeechRecognizer()
        self.conversation = Conversation(self.recognizer)

    def get_latest_time(self):
        # Returns the latest meeting end time
        return max(self.meetings_end_time)

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

    async def create_meeting_session(self, start_time: str, end_time: str):
        """
        Asynchronously schedules tasks for managing a meeting session.

        Joining and leaving a meeting is performed asynchronously. This is chosen because real-time transcription
        starts another loop. multiprocessing to improve performance does not work.

         Args:
            start_time (str): Meeting start time in "HH:MM" format.
            end_time (str): Meeting end time in "HH:MM" format.
        """

        # Add the meeting end time to the list of end times
        self.meetings_end_time.append(
            datetime.strptime(end_time, "%H:%M")
        )

        # Schedule the recording to start at the specified start time
        self.schedule.every().day.at(start_time).do(self.handle_recording)

        # Schedule joining the conversation 5 minutes after the start time
        self.schedule.every().day.at(
            (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        ).do(create_async_task, self.conversation.join)

        # Schedule quitting the conversation at the specified end time
        self.schedule.every().day.at(end_time).do(create_async_task, self.conversation.quit)

        # Schedule stopping the recording 5 minutes after the end time
        self.schedule.every().day.at(
            (datetime.strptime(end_time, "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        ).do(self.handle_recording)
