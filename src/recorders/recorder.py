import threading

from moviepy.editor import AudioFileClip, VideoFileClip

from configs import config
from src.recorders.audio_recorder import AudioRecorder
from src.recorders.video_recorder import VideoRecorder
from src.utils.create_filenames import create_filenames


class Recorder:
    """
    A class for managing simultaneous audio and video recording.

    Attributes:
        audio_recorder (AudioRecorder): Instance of the audio recorder.
        video_recorder (VideoRecorder): Instance of the video recorder.
        audio_thread (Thread): Thread for running the audio recording process.
        video_thread (Thread): Thread for running the video recording process.
    """

    def __init__(self):
        """
        Initializes the recorder with separate threads for audio and video recording.
        """
        self.audio_recorder = AudioRecorder()  # Initialize audio recorder
        self.video_recorder = VideoRecorder()  # Initialize video recorder
        
        # Create separate threads for audio and video recording
        self.audio_thread = threading.Thread(target=self.audio_recorder.record_audio)
        self.video_thread = threading.Thread(target=self.video_recorder.record_screen)
    
    def start_record(self):
        """
        Starts both audio and video recording in separate threads.
        """
        self.audio_thread.start()  # Start audio recording thread
        self.video_thread.start()  # Start video recording thread
    
    def stop_record(self):
        """
        Stops the recording process for both audio and video.

        - Ensures that both threads are properly terminated.
        - Calls `create_finale_video` to merge audio and video into a final file.
        """
        self.audio_recorder.record_stop()  # Stop audio recording
        self.video_recorder.record_stop()  # Stop video recording
        
        self.audio_thread.join()  # Wait for the audio recording thread to finish
        self.video_thread.join()  # Wait for the video recording thread to finish
        
        self.create_finale_video()  # Merge audio and video into a single file
        
    def create_finale_video(self):
        """
        Synchronizes and merges the recorded audio and video into a single MP4 file.

        - Adjusts the duration of the video and audio to the shortest length.
        - Saves the final video file in the `videofiles` directory.
        - Deletes the temporary raw video file after merging.
        """
        video_clip = VideoFileClip(self.video_recorder.VIDEO_PATH)
        audio_clip = AudioFileClip(self.audio_recorder.AUDIO_PATH)
        
        # Ensure both clips have the same duration
        min_duration = min(video_clip.duration, audio_clip.duration)
        video_clip = video_clip.subclip(0, min_duration)
        audio_clip = audio_clip.subclip(0, min_duration)

        # Merge audio with video
        final_clip = video_clip.set_audio(audio_clip)
        final_output_path = f"{config.BASE_DIR}/data/videofiles/{create_filenames()}.mp4"
        final_clip.write_videofile(final_output_path, codec="libx264", audio_codec="aac", fps=30)
        
        # Delete temporary video file to save space
        self.video_recorder.del_temp_video()
