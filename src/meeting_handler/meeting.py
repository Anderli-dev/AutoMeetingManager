from datetime import datetime, timedelta

import schedule

from src.conversation.conversation import Conversation
from src.recorders.recorder import Recorder


class MeetingHandler:
    def __init__(self):
        # List to store meeting end times
        self.meetings_end_time = []

        self.schedule = schedule.Scheduler()
        self.conversation = Conversation()
        self.recorder = Recorder()

    def get_latest_time(self):
        # Returns the latest meeting end time
        return max(self.meetings_end_time)


    def create_meeting_session(self, start_time: str, end_time: str):
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
        self.schedule.every().day.at(start_time).do(self.recorder.start_record)

        # Schedule joining the conversation 5 minutes after the start time
        self.schedule.every().day.at(
            (datetime.strptime(start_time, "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        ).do(self.conversation.join)

        # Schedule quitting the conversation at the specified end time
        self.schedule.every().day.at(end_time).do(self.conversation.quit)

        # Schedule stopping the recording 5 minutes after the end time
        self.schedule.every().day.at(
            (datetime.strptime(end_time, "%H:%M") + timedelta(minutes=5)).strftime("%H:%M")
        ).do(self.recorder.stop_record)
