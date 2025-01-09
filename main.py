import os
import time
from datetime import datetime, timedelta

from MeetingHandler import MeetingHandler
from get_filenames import get_filenames
from make_audio import make_audio
from transcription import audio_transcription

if __name__ == "__main__":
    # Initialize the meeting handler
    meeting_handler = MeetingHandler()

    # Schedule the join and quit functions for the meeting at specific times
    # TODO: Extend functionality for scheduling across multiple days
    meeting_handler.create_meeting_session("08:05", "09:35")

    # Main loop to execute scheduled tasks and handle meeting lifecycle
    try:
        while True:
            # Get the current time
            current_time = datetime.now().time()

            # Check if the program should stop running
            # TODO: Fix handling when the meeting ends after midnight (next day)
            # !!!IMPORTANT!! Time is the latest meeting end time + 10 minutes
            if current_time >= (meeting_handler.get_latest_time() + timedelta(minutes=10)).time():
                print("Meetings have ended. Time to make transcription.")
                break

            # Run all pending scheduled tasks
            meeting_handler.schedule.run_pending()
            time.sleep(1)

        # Retrieve filenames of the videos recorded today
        today_videos_filenames = get_filenames()

        # Convert recorded video files into audio files
        make_audio(today_videos_filenames)

        # Perform transcription on the generated audio files
        audio_transcription(today_videos_filenames)

        # Wait for 5 minutes before shutting down the system
        time.sleep(60 * 5)
        os.system("shutdown /s /t 1")

    # Handle manual interruption (e.g., Ctrl+C)
    except KeyboardInterrupt:
        print("\nProgram terminated.")
