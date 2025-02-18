import time
import wave

import numpy as np
import sounddevice as sd

from configs import config
from src.utils.create_filenames import create_filenames


class AudioRecorder:
    def __init__(self):
        self.audio_frames = []
        self.sample_rate = 44100
        self.channels = 2
        self.AUDIO_PATH = f"{config.BASE_DIR}/data/audiofiles/{create_filenames()}.wav"
        self.is_recording = True
        self.start_time = None
        
    def _callback(self, indata, frames, time_info, status):
        if status:
            print(status)
        self.audio_frames.append(indata.copy())
    
    def record_audio(self):
            self.start_time = time.time()
            with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._callback):
                while self.is_recording:
                    time.sleep(0.1)
            self._save_audio()
                
    def _save_audio(self):
        with wave.open(self.AUDIO_PATH, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-бітне аудіо
            wf.setframerate(self.sample_rate)
            for frame in self.audio_frames:
                wf.writeframes(np.int16(frame * 32767).tobytes())
                
    def record_stop(self):
        self.is_recording = False