import asyncio
import threading

import schedule
from rapidfuzz import process
from RealtimeSTT import AudioToTextRecorder

from src.audio_to_text_transcriber.audio_to_text_transcriber import \
    AudioToTextTranscriber
from src.bot.handlers import send_message_to_user
from src.utils.escape_special_characters import escape_special_characters
from configs.config import LANGUAGE, SEARCH_WORDS, WHISPER_PROMPT

class WordSearcher:
    def __init__(self, search_words):
        # Initialize with a list of words to search for
        self.search_words = search_words

    def search_in_sentence(self, sentence):
        # Split the sentence into words for processing
        words = sentence.split(" ")

        # Loop through each search word
        for search_word in self.search_words:
            # Perform fuzzy matching using rapidfuzz
            matches = process.extract(search_word, words)

            # Filter matches with a similarity score greater than 80%
            for match in matches:
                if len(match[0]) >= len(search_word) - 1 and match[1] > 80:  # Only 80% match, no less
                    word = escape_special_characters(match[0])
                    similarity = escape_special_characters(str(match[1]))
                    sentence = escape_special_characters(sentence)
                    
                    asyncio.run(
                        send_message_to_user(
                            f"You have been mentioned\!\n"
                            f"Word: {search_word} \({word}\)\.\n"
                            f"Similarity: {similarity}\.\n"
                            f">{sentence}\n"
                            f"__Audio will be added__\n"
                            f"__Video will be added__")
                        )


class SpeechProcessor:
    def __init__(self, searcher):
        # Initialize with a WordSearcher instance
        self.searcher = searcher

    def text_detected(self, text):
        # Handle incomplete sentences detected during real-time transcription
        pass
        # Code below use only for debug purpose
        # print(text)
        # thread = threading.Thread(target=self.searcher.search_in_sentence, args=(text,))
        # thread.start()

    def process_text(self, text):
        # Handle complete and processed sentences
        thread = threading.Thread(target=self.searcher.search_in_sentence, args=(text,))
        thread.start()


class RealtimeSpeechRecognizer:
    def __init__(self):
        """
        A class for managing real-time speech recognition with keyword searching and transcription.
        """
        # List of keywords to search for in the transcription
        self.searcher = WordSearcher(SEARCH_WORDS)
        self.processor = SpeechProcessor(self.searcher)
        self.schedule = schedule
        self.recorder_is_running = True
        # Configuration for the audio-to-text recorder
        self.recorder_config = {
            'spinner': False,  # Disable spinner for real-time transcription
            'model': 'medium',  # Specify model type (medium in this case)
            # TODO: Implement auto-indexing for input devices (RealtimeSTT uses PyAudio)
            'input_device_index': 0,  # Specify the input device index
            'realtime_model_type': 'medium',  # Model type for real-time transcription
            'language': LANGUAGE,  # Language set to Ukrainian
            'silero_sensitivity': 0.05,  # Sensitivity for Silero VAD
            'webrtc_sensitivity': 3,  # Sensitivity for WebRTC
            'post_speech_silence_duration': 0.7,  # Silence duration to consider as the end of speech
            'min_length_of_recording': 1.1,  # Minimum length of recording in seconds
            'min_gap_between_recordings': 0,  # Minimum gap between consecutive recordings
            'enable_realtime_transcription': True,  # Enable real-time transcription
            'realtime_processing_pause': 0.02,  # Pause duration between real-time processing
            'on_realtime_transcription_update': self.processor.text_detected,  # Callback for partial transcription
            'silero_deactivity_detection': True,  # Enable Silero activity detection
            'early_transcription_on_silence': 0,  # Trigger early transcription on silence
            'beam_size': 5,  # Beam size for full transcription
            'beam_size_realtime': 3,  # Beam size for real-time transcription
            'no_log_file': True,  # Disable log file creation
            'initial_prompt': WHISPER_PROMPT
        }
        # Initialize the recorder
        self.recorder = None
        self.is_recording = True

    def start_recorder(self):
        print("AudioToTextRecorder start")
        self.recorder = AudioToTextTranscriber(**self.recorder_config)
        while self.is_recording:
            # Process real-time transcription with the provided processor
            self.recorder.text(self.processor.process_text)

    def shutdown(self):
        # Stops the recorder and cleans up resources.
        self.recorder.shutdown()
        
        # Stoping of Transcriber loop
        self.is_recording = False
        
        print("AudioToTextRecorder shutdown")
