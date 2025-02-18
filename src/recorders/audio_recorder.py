import time
import wave

import numpy as np
import sounddevice as sd

from configs import config
from src.utils.create_filenames import create_filenames


class AudioRecorder:
    def __init__(self):
        """
        Class for recording audio of PC and saving it as a WAV file.

        Attributes:
            audio_frames (list): List of recorded audio frames.
            sample_rate (int): Sampling rate of the audio (default: 44100 Hz).
            channels (int): Number of audio channels (default: 2 - stereo).
            AUDIO_PATH (str): File path where the recorded audio will be saved.
            is_recording (bool): Flag to control recording state.
            start_time (float): Timestamp when the recording starts.
        """
        self.audio_frames = []
        self.sample_rate = 44100  # Standard high-quality audio sampling rate
        self.channels = 2  # Stereo recording
        self.AUDIO_PATH = f"{config.BASE_DIR}/data/audiofiles/{create_filenames()}.wav"
        self.is_recording = True
        self.start_time = None
        
    def _callback(self, indata, frames, time_info, status):
        """
        Callback function that captures audio input.

        Args:
            indata (numpy.ndarray): Incoming audio data.
            frames (int): Number of frames per buffer.
            time_info (dict): Time-related information about the audio stream.
            status (sounddevice.CallbackFlags): Status of the audio stream.
        """
        if status:
            print("Audio error:", status)  # Print any errors if they occur
        self.audio_frames.append(indata.copy())  # Append the recorded audio data
    
    def record_audio(self):
        """
        Starts the recording process, continuously capturing audio data.

        The function keeps recording until `self.is_recording` is set to False.
        """
        self.start_time = time.time()  # Store the recording start time
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, callback=self._callback):
            while self.is_recording:
                sd.sleep(100)  # Using "sd" for better performance
        self._save_audio()  # Save the recorded audio after stopping
                
    def _save_audio(self):
        """
        Saves the recorded audio frames to a WAV file.
        """
        with wave.open(self.AUDIO_PATH, "wb") as wf:
            wf.setnchannels(self.channels)  # Set number of channels (stereo)
            wf.setsampwidth(2)  # 16-bit audio format
            wf.setframerate(self.sample_rate)  # Set the sample rate
            for frame in self.audio_frames:
                wf.writeframes(np.int16(frame * 32767).tobytes())  # Convert and save audio data
                
    def record_stop(self):
        """
        Stops the recording process.
        """
        self.is_recording = False
