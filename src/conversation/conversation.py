import time

import pyautogui


class Conversation:
    def __init__(self, recognizer):
        """
            A class for handling conversation join and quit operations, integrated with speech recognition.
        """
        self.recognizer = recognizer

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
        # Note: Due to threading conflicts with some libraries, multiprocessing is not used here.
        self.recognizer.start_recorder()

    # Function to quit the conversation
    def quit(self):
        # Stop the speech recognition recorder
        self.recognizer.shutdown()

        # Close the current tab to exit the conversation
        pyautogui.hotkey('ctrl', 'f4')
        time.sleep(0.5)
