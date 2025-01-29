import gc
import logging

from RealtimeSTT import AudioToTextRecorder


class AudioToTextTranscriber(AudioToTextRecorder):
    def shutdown(self):
        """
        Safely shuts down the audio recording process, ensuring that all worker threads,
        processes, and resources are properly terminated and released.
        """

        # Acquire a lock to ensure thread safety during shutdown
        with self.shutdown_lock:
            # If the shutdown process has already been initiated, exit early
            if self.is_shut_down:
                return

            # Display a shutdown message in the console for visual feedback
            print("\033[91mRealtimeSTT shutting down\033[0m")

            # Mark the recorder as shut down and signal all active events to stop
            self.is_shut_down = True
            self.start_recording_event.set()
            self.stop_recording_event.set()
            self.shutdown_event.set()
            self.is_recording = False
            self.is_running = False

            # Log and terminate the recording thread
            logging.debug('Finishing recording thread')
            if self.recording_thread:
                self.recording_thread.join()

            # Log and terminate the reader process responsible for audio input
            logging.debug('Terminating reader process')
            if self.use_microphone.value:
                self.reader_process.join(timeout=10)

                # If the reader process does not terminate within the timeout, force terminate it
                if self.reader_process.is_alive():
                    logging.warning("Reader process did not terminate "
                                    "in time. Terminating forcefully.")
                    self.reader_process.terminate()

            # Log and terminate the transcription process responsible for processing audio
            logging.debug('Terminating transcription process')
            self.transcript_process.join(timeout=10)

            # If the transcription process does not terminate within the timeout, force terminate it
            if self.transcript_process.is_alive():
                logging.warning("Transcript process did not terminate "
                                "in time. Terminating forcefully.")
                self.transcript_process.terminate()

            # Close the communication pipe used for transcription
            self.parent_transcription_pipe.close()

            # Log and terminate the real-time processing thread
            logging.debug('Finishing realtime thread')
            if self.realtime_thread:
                self.realtime_thread.join()

            # Perform garbage collection to free up memory
            gc.collect()
