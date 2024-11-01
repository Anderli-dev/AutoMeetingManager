from moviepy.editor import VideoFileClip


def make_audio(video_filenames: list):
    # Iterate over each video file in the list to convert to audio
    for vf in video_filenames:
        # Define the path to the video file and the output path for the audio file
        path_to_video_file = f"C:/Users/lolke/Videos/OBS/{vf[0]}"
        filename = vf[0].split(".")[0]  # Extract the filename without extension
        path_to_audio_file = f"audiofiles/{filename}.mp3"  # Set the output path for the audio file

        # Load the video clip from the specified file
        video_clip = VideoFileClip(path_to_video_file)

        # Extract the audio part from the video clip
        audio_clip = video_clip.audio

        # Write the extracted audio to a separate .mp3 file
        audio_clip.write_audiofile(path_to_audio_file)

        # Close the audio and video clips to release resources
        audio_clip.close()
        video_clip.close()

        # Confirmation message for successful audio extraction
        print(f"Audio from {filename} extracted successfully!")
