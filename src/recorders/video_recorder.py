
import os
import time
import cv2
import mss
import numpy as np

from configs import config
from src.utils.create_filenames import create_filenames


class VideoRecorder:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.fps = 30
        self.VIDEO_PATH = f"{config.BASE_DIR}/data/{create_filenames()}.mkv"
        self.is_recording = True
        self.start_time = None
        self.frame_timestamps = []

    
    def record_screen(self):
        self.start_time = time.time()
        frame_count = 0
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.VIDEO_PATH, fourcc, self.fps, (self.screen_width, self.screen_height))

        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": self.screen_width, "height": self.screen_height}

            while self.is_recording:
                frame_time = time.time()
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)

                frame_count += 1
                elapsed = time.time() - frame_time
                expected_time = frame_count / self.fps
                actual_time = time.time() - self.start_time
                correction = expected_time - actual_time

                # Враховуємо накопичені затримки
                sleep_time = max(0, (1 / self.fps) + correction)
                time.sleep(sleep_time)

        self.duration = time.time() - self.start_time
        out.release()
        
    def del_temp_video(self):
        if os.path.exists(self.VIDEO_PATH):
            os.remove(self.VIDEO_PATH)
    
    def record_stop(self):
        self.is_recording = False
