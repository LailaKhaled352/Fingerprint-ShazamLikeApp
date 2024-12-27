import os
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage import maximum_filter
from hashlib import sha256

class Features:
    def __init__(self):
        self.input_folder = "Spectrograms"
        self.feature_folder = "Features"
        self.hash_folder = "Hashes"
        os.makedirs(self.feature_folder, exist_ok=True)
        os.makedirs(self.hash_folder, exist_ok=True)


    # Function to extract main features from a spectrogram
    def extract_features(self, spectrogram, threshold=0.5):
        max_filtered = maximum_filter(spectrogram, size=10)
        peaks = (spectrogram == max_filtered) & (spectrogram > threshold * np.max(spectrogram))

        feature_indices = np.argwhere(peaks)
        feature_values = spectrogram[peaks]

        # Combine indices and values
        features = np.hstack((feature_indices, feature_values[:, None]))
        return features




    #THIS IS WRITTEN TO BE EXECUTED ONCE
    def extract_and_save_75_features(self):
        # Process each spectrogram
        for filename in os.listdir(self.input_folder):
            if filename.endswith(".npy"):
                file_path = os.path.join(self.input_folder, filename)
                spectrogram = np.load(file_path)

                # Extract features
                features = self.extract_features(spectrogram)

                # Save features to feature folder
                feature_path = os.path.join(self.feature_folder, filename)
                np.save(feature_path, features)

        print("Feature extraction complete. Files saved in:", self.feature_folder)


    #THIS IS WRITTEN TO BE EXECUTED ONCE
    def generate_and_save_75_hashes(self):
        # Process each feature file
        for filename in os.listdir(self.feature_folder):
            if filename.endswith(".npy"):
                file_path = os.path.join(self.feature_folder, filename)
                features = np.load(file_path)

                # Generate perceptual hash by hashing the features
                feature_hash = sha256(features.tobytes()).hexdigest()

                # Save the hash to the hash folder
                hash_path = os.path.join(self.hash_folder, f"{os.path.splitext(filename)[0]}_hash.txt")
                with open(hash_path, "w") as hash_file:
                    hash_file.write(feature_hash)

        print("Hash generation complete. Files saved in:", self.hash_folder)

    def generate_hash(self, features):
        return sha256(features.tobytes()).hexdigest()
    