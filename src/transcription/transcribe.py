from faster_whisper import WhisperModel
from configs import config


def audio_transcription(audio_filenames: list):
    # Specify the model size for Whisper (large-v3) and set it to run on GPU with FP16 precision
    model_size = "large-v3"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # Print start message for transcription process
    print("Begin of transcription")

    # Iterate over each audio file in the list for transcription
    for af in audio_filenames:
        # Extract the filename without the extension for easier access and display
        filename = af[0].split(".")[0]
        print(f"Transcription of {filename}")

        # Transcribe the audio file with specified beam size and language set to Ukrainian ("uk")
        segments, info = model.transcribe(f"{config.BASE_DIR}/data/audiofiles/{filename}.wav", beam_size=5, language="uk")

        # Open a new text file for saving the transcription results
        with open(f"{config.BASE_DIR}/data/transcriptions/{filename} transcription.txt", "w", encoding="utf-8") as file:
            # Write each segment's start time, end time, and text to the file
            for segment in segments:
                line = segment.text + " \n"
                file.write(line)
