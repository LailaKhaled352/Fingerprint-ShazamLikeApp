from PyQt5.QtWidgets import QFileDialog
from pydub import AudioSegment
import os

class Browse:
    def __init__(self):
        pass

    def open_file_dialog(self, label):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(None, "Select WAV File", "", "WAV Files (*.wav);;All Files (*)", options=options)
        
        if file_path:
            # Display the file name on the label
            label.setText(os.path.basename(file_path))

            # Check and process the file
            processed_path = self.process_file(file_path)
            return processed_path  # Return the processed file path
        return None

    def process_file(self, file_path):
        # Load the audio file
        audio = AudioSegment.from_file(file_path)

        # Check if the duration exceeds 30 seconds
        duration_ms = len(audio)  # Duration in milliseconds
        if duration_ms > 30 * 1000:  # 30 seconds in milliseconds
            # Trim to the first 30 seconds
            trimmed_audio = audio[:30 * 1000]

            # Save the trimmed audio to a temporary file
            output_path = os.path.splitext(file_path)[0] + "_trimmed.wav"
            trimmed_audio.export(output_path, format="wav")
            print(f"File trimmed to 30 seconds and saved as: {output_path}")
            return output_path

        print("File is already 30 seconds or shorter.")
        return file_path  # Return the original file path if no trimming was needed
