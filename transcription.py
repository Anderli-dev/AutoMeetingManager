from faster_whisper import WhisperModel

# Specify the model size for Whisper (large-v3) and set it to run on GPU with FP16 precision
model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")


def audio_transcription(audio_filenames: list):
    # Print start message for transcription process
    print("Begin of transcription")

    # Iterate over each audio file in the list for transcription
    for af in audio_filenames:
        # Extract the filename without the extension for easier access and display
        filename = af[0].split(".")[0]
        print(f"Transcription of {filename}")

        # Transcribe the audio file with specified beam size and language set to Ukrainian ("uk")
        segments, info = model.transcribe(f"audiofiles/{filename}.mp3", beam_size=5, language="uk")

        # Open a new text file for saving the transcription results
        with open(f"{filename} transcription.txt", "w", encoding="utf-8") as file:
            # Write each segment's start time, end time, and text to the file
            for segment in segments:
                line = "[%.2fs -> %.2fs] %s \n" % (segment.start, segment.end, segment.text)
                file.write(line)
