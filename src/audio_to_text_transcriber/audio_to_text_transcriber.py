import gc
import logging

from RealtimeSTT import AudioToTextRecorder


class AudioToTextTranscriber(AudioToTextRecorder):
    def shutdown(self):
        """
        Safely shuts down the audio recording by stopping the
        recording worker and closing the audio stream.
        """

        with self.shutdown_lock:
            if self.is_shut_down:
                return

            print("\033[91mRealtimeSTT shutting down\033[0m")
            # logging.debug("RealtimeSTT shutting down")

            # Force wait_audio() and text() to exit
            self.is_shut_down = True
            self.start_recording_event.set()
            self.stop_recording_event.set()

            self.shutdown_event.set()
            self.is_recording = False
            self.is_running = False

            logging.debug('Finishing recording thread')
            if self.recording_thread:
                self.recording_thread.join()

            logging.debug('Terminating reader process')

            # Give it some time to finish the loop and cleanup.
            if self.use_microphone.value:
                self.reader_process.join(timeout=10)

                if self.reader_process.is_alive():
                    logging.warning("Reader process did not terminate "
                                    "in time. Terminating forcefully."
                                    )
                    self.reader_process.terminate()

            logging.debug('Terminating transcription process')
            self.transcript_process.join(timeout=10)

            if self.transcript_process.is_alive():
                logging.warning("Transcript process did not terminate "
                                "in time. Terminating forcefully."
                                )
                self.transcript_process.terminate()

            self.parent_transcription_pipe.close()

            logging.debug('Finishing realtime thread')
            if self.realtime_thread:
                self.realtime_thread.join()

            if self.enable_realtime_transcription:
                if self.realtime_model_type:
                    # The commented code is present in the class that is being used.
                    # This code terminates the execution of the program.

                    # del self.realtime_model_type

                    logging.debug("Model set none")
                    self.realtime_model_type = None

            gc.collect()
