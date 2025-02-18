

import threading

from moviepy.editor import AudioFileClip, VideoFileClip

from configs import config
from src.recorders.audio_recorder import AudioRecorder
from src.recorders.video_recorder import VideoRecorder
from src.utils.create_filenames import create_filenames


class Recorder:
    def __init__(self):
        self.audio_recorder = AudioRecorder()
        self.video_recorder = VideoRecorder()
        
        self.audio_thread = threading.Thread(target=self.audio_recorder.record_audio)
        self.video_thread = threading.Thread(target=self.video_recorder.record_screen)
    
    def start_record(self):
        self.audio_thread.start()
        self.video_thread.start()
    
    def stop_record(self):
        self.audio_recorder.record_stop()
        self.video_recorder.record_stop()
        
        self.audio_thread.join()
        self.video_thread.join()
        
        self.create_finale_video()
        
    def create_finale_video(self):
        video_clip = VideoFileClip(self.video_recorder.VIDEO_PATH)
        audio_clip = AudioFileClip(self.audio_recorder.AUDIO_PATH)
        
        min_duration = min(video_clip.duration, audio_clip.duration)
        video_clip = video_clip.subclip(0, min_duration)
        audio_clip = audio_clip.subclip(0, min_duration)

        
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(f"{config.BASE_DIR}/data/videofiles/{create_filenames()}.mp4", codec="libx264", audio_codec="aac", fps=30)
        
        self.video_recorder.del_temp_video()     
    