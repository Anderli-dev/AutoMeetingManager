import threading
import time

import pyautogui

from src.realtime_recognizer.realtime_speech_recognizer import \
    RealtimeSpeechRecognizer


class Conversation:
    def __init__(self):
        """
            A class for handling conversation join and quit operations, integrated with speech recognition.
        """
        self.recognizer = RealtimeSpeechRecognizer()
        self.recording = None

    # Function to handle mouse manipulations for joining a conversation
    def join(self):
        # Move mouse to the "Join" button of the conversation application and click it
        pyautogui.moveTo(700, 590)
        pyautogui.click(button='left')
        time.sleep(2.5)

        # Move mouse to the "Video" button and enable video
        pyautogui.moveTo(765, 740)
        pyautogui.click(button='left')
        time.sleep(0.5)

        # Move mouse to the "Mic" button to enable microphone
        pyautogui.moveTo(685, 740)
        pyautogui.click(button='left')
        time.sleep(0.5)

        # Switch to the previous tab using keyboard shortcut to adjust focus
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(0.5)

        # Close the current tab if it's no longer needed
        pyautogui.hotkey('ctrl', 'f4')
        time.sleep(0.5)

        # Move mouse to another "Join" button if present and click it to fully join the conversation
        pyautogui.moveTo(1340, 635)
        pyautogui.click(button='left')
        time.sleep(0.5)

        # Start the speech recognition recorder in a separate thread
        # Each time a Thread must be created and closed manually
        # NOTE: multiprocessing does not work due to the nature of RSTT
        self.recording = threading.Thread(target=self.recognizer.start_recorder)
        self.recording.start()

    # Function to quit the conversation
    def quit(self):
        # Stop the speech recognition recorder
        self.recognizer.shutdown()
        
        # Closing a thread
        self.recording.join()
        self.recording = None

        # Close the current tab to exit the conversation
        pyautogui.hotkey('ctrl', 'f4')
        time.sleep(0.5)
