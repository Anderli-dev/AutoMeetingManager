import time
import wave

import numpy as np
import sounddevice as sd

from configs import config
from src.utils import create_filenames


class AudioRecorder:
    def __init__(self):
        self.audio_frames = []
        self.sample_rate = 44100
        self.chanels = 2
        self.AUDIO_PATH = f"{config.BASE_DIR}/data/transcriptions/{create_filenames()}.wav"
        self.is_recording = True
        
    def _callback(self, indata, frames, time, status):
            if status:
                print(status)
            self.audio_frames.append(indata.copy())
    
    def record_audio(self):
        """Функція для запису звуку"""
        with sd.InputStream(samplerate=self.sample_rate, channels=self.chanels, callback=self._callback):
            print("Аудіозапис почався...")
            while self.is_recording:
                time.sleep(0.1)
                
    def save_audio(self):
        """Збереження аудіо у файл"""
        wf = wave.open(self.AUDIO_PATH, "wb")
        wf.setnchannels(self.chanels)
        wf.setsampwidth(2)  # 16-бітне аудіо
        wf.setframerate(self.sample_rate)
        wf.writeframes(b"".join([np.int16(frame * 32767).tobytes() for frame in self.audio_frames]))
        wf.close()
        
    def record_stop(self):
        self.is_recording = False