import os
from datetime import datetime, timedelta
from typing import NoReturn
import time

from src.meeting_handler.meeting import MeetingHandler
from src.transcription.transcribe import audio_transcription
from src.utils.audio_converter import audio_converter
from src.utils.get_filenames import get_filenames


def run_schedule(meeting_handler):
    while True:
        # Retrieve the current time
        current_time = datetime.now().time()

        # Check if the current time has surpassed the latest meeting end time plus 10 minutes
        # TODO: Address issues when meetings extend past midnight (next day).
        # !!!IMPORTANT!! Ensure 'get_latest_time' accommodates meeting schedules properly.
        if current_time >= (meeting_handler.get_latest_time() + timedelta(minutes=10)).time():
            print("Meetings have ended. Time to make transcription.")
            break

        # Execute all pending tasks in the meeting scheduler
        meeting_handler.schedule.run_pending()
        time.sleep(1)


def main() -> NoReturn:
    # Create an instance of the meeting handler
    meeting_handler = MeetingHandler()

    # Schedule a sample meeting session (start and end times dynamically adjusted for testing)
    # TODO: Add functionality to manage multi-day scheduling for meetings.
    # meeting_handler.create_meeting_session("13:10", "13:20")
    meeting_handler.create_meeting_session(
        (datetime.strptime(datetime.now().time().strftime("%H:%M"), "%H:%M") + timedelta(minutes=2)).strftime("%H:%M"),
        (datetime.strptime(datetime.now().time().strftime("%H:%M"), "%H:%M") + timedelta(minutes=8)).strftime("%H:%M"))
    print("Start time:"+(datetime.strptime(datetime.now().time().strftime("%H:%M"), "%H:%M") + timedelta(minutes=2)).strftime("%H:%M"))
    print("End time:"+(datetime.strptime(datetime.now().time().strftime("%H:%M"), "%H:%M") + timedelta(minutes=7)).strftime("%H:%M"))

    # Main loop to execute scheduled tasks and handle the meeting lifecycle
    try:
        run_schedule(meeting_handler)

        # Retrieve filenames of video recordings created today
        today_videos_filenames = get_filenames()

        # Convert recorded video files to audio format
        audio_converter(today_videos_filenames)

        # Perform transcription on the audio files
        audio_transcription(today_videos_filenames)

        # Wait for 5 minutes before initiating system shutdown
        time.sleep(60 * 5)
        os.system("shutdown /s /t 1")

    # Handle manual interruption (e.g., Ctrl+C)
    except KeyboardInterrupt:
        print("\nProgram terminated by keyboard interrupt.")

        # Closing program after using recognizer. Without this wil be infinity loop and program doesn't end
        del meeting_handler.recognizer.recorder.realtime_model_type
        meeting_handler.recognizer.recorder.realtime_model_type = None

    except Exception as e:
        print(e)