import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from ExtractFeaturesAndHahsing import ExtractFeaturesAndHahsing
from Spectrogram import Spectrogram

import os
import numpy as np
from scipy.spatial.distance import hamming
from tabulate import tabulate

class SimilaritySearch:
    def __init__(self):
        self.feature_hashing= ExtractFeaturesAndHahsing ()
        self.spectrogram = Spectrogram()
        self.hash_folder = self.feature_hashing.hash_folder

    def generate_hash_for_file(self, file_path):
        spectrogram = self.spectrogram.extract_spectrogram(file_path)
        features = self.feature_hashing.extract_features(spectrogram)
        file_hash = self.feature_hashing.features_phash(features)
        return file_hash

    def compute_similarity(self, target_hash, hash_list):
        similarities = []
        for file_name, file_hash in hash_list:
            if target_hash and file_hash:
                distance = hamming(list(target_hash), list(file_hash))
                similarity = 1 - distance  # Convert to similarity index
                similarities.append((file_name, similarity))
        return sorted(similarities, key=lambda x: x[1], reverse=True)

    def load_precomputed_hashes(self):
        hash_list = []
        for hash_file in os.listdir(self.hash_folder):
            if hash_file.endswith("_hash.txt"):
                file_path = os.path.join(self.hash_folder, hash_file)
                with open(file_path, "r") as f:
                    file_hash = f.read().strip()
                    hash_list.append((hash_file.replace("_hash.txt", ""), file_hash))
        return hash_list

    def search_similarity(self, file_path):
        # Generate the hash for the input file
        target_hash = self.generate_hash_for_file(file_path)

        # Load precomputed hashes
        precomputed_hashes = self.load_precomputed_hashes()

        # Compute similarities
        sorted_similarities = self.compute_similarity(target_hash, precomputed_hashes)

        # Display results in a table
        #print("Similarity Results:")
       # print(tabulate(sorted_similarities, headers=["File Name", "Similarity Index"], tablefmt="grid"))
        return sorted_similarities

    def search_similarity_for_mixed_file(self, file_path1, file_path2, slider_value):
        # Generate a mixed spectrogram
        mixed_spectrogram = self.spectrogram.mix_spectrograms(file_path1, file_path2, slider_value)
        
        # Save mixed spectrogram as a temporary file
        temp_file = "temp_mixed.npy"
        np.save(temp_file, mixed_spectrogram)

        # Generate hash for the mixed spectrogram
        features = self.feature_hashing.extract_features(mixed_spectrogram)
        mixed_file_hash = self.feature_hashing.features_phash(features)

        # Load precomputed hashes
        precomputed_hashes = self.load_precomputed_hashes()

        # Compute similarities
        sorted_similarities = self.compute_similarity(mixed_file_hash, precomputed_hashes)

        # Display results in a table
        #print("Similarity Results for Mixed File:")
        #print(tabulate(sorted_similarities, headers=["File Name", "Similarity Index"], tablefmt="grid"))

        # Clean up temporary file
        os.remove(temp_file)
        return sorted_similarities
