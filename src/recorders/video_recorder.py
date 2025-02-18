import os
import time

import cv2
import mss
import numpy as np

from configs import config
from src.utils.create_filenames import create_filenames


class VideoRecorder:
    """
    A class for screen recording using MSS and OpenCV.

    Attributes:
        screen_width (int): Width of the screen to capture.
        screen_height (int): Height of the screen to capture.
        fps (int): Frames per second for the video recording.
        VIDEO_PATH (str): Path to save the recorded video file.
        is_recording (bool): Flag to control the recording process.
        start_time (float): Timestamp when recording starts.
        frame_timestamps (list): List to store timestamps of captured frames.
    """

    def __init__(self):
        """
        Initializes the video recorder with screen size, frame rate, and output file path.
        """
        self.screen_width = 1920  # Set screen width for recording
        self.screen_height = 1080  # Set screen height for recording
        self.fps = 30  # Frames per second for smooth recording
        self.VIDEO_PATH = f"{config.BASE_DIR}/data/{create_filenames()}.mkv"
        self.is_recording = True
        self.start_time = None
        self.frame_timestamps = []

    def record_screen(self):
        """
        Starts screen recording using MSS for screen capture and OpenCV for saving video.
        """
        self.start_time = time.time()  # Store the recording start time
        frame_count = 0

        # Define video codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.VIDEO_PATH, fourcc, self.fps, (self.screen_width, self.screen_height))

        with mss.mss() as sct:
            # Define the screen area to capture
            monitor = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}

            while self.is_recording:
                frame_time = time.time()  # Timestamp before capturing the frame
                
                # Capture the screen frame
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert BGRA to BGR format
                out.write(frame)  # Save frame to the video file

                frame_count += 1
                elapsed = time.time() - frame_time
                expected_time = frame_count / self.fps  # Expected time based on FPS
                actual_time = time.time() - self.start_time  # Actual elapsed time
                correction = expected_time - actual_time  # Calculate correction time

                # Adjust sleep time to maintain consistent FPS
                sleep_time = max(0, (1 / self.fps) + correction)
                time.sleep(sleep_time)

        self.duration = time.time() - self.start_time  # Calculate recording duration
        out.release()  # Release the video writer

    def del_temp_video(self):
        """
        Deletes the recorded video (without sound) file.
        """
        if os.path.exists(self.VIDEO_PATH):
            os.remove(self.VIDEO_PATH)

    def record_stop(self):
        """
        Stops the recording process.
        """
        self.is_recording = False
