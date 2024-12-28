from scipy.signal import spectrogram
import numpy as np
import os
from scipy.io import wavfile
class Spectrogram:
    def __init__(self):
        pass

    def find_spectrogram(self, data, sample_rate):
        f, t, Sxx = spectrogram(data, sample_rate) #f: frequency, t: time, Sxx, spectrogram matrix
        Sxx_dB = 10 * np.log10(Sxx + np.finfo(float).eps) #np.finfo is to avoid take log(0)
        return Sxx_dB
    
    def load_spectrograms(self,source_folder):
        spectrograms=[]
        file_names=[]
        for file_name in os.listdir(source_folder):
            if file_name.endswith('.npy'):  
                file_path = os.path.join(source_folder, file_name)
                spectrogram= np.load(file_path)
                spectrograms.append(spectrogram)
                file_names.append(file_name)
        return spectrograms, file_names
    
        
    def extract_spectrogram(self, file_path):
        sample_rate, song = wavfile.read(file_path)
        duration=30
        num_samples = min(duration * sample_rate, len(song))
        if len(song.shape) == 1:
            song_data = song[:num_samples] 
        elif len(song.shape) >1 :
            song_data = song[:num_samples,0]
        Sxx_dB= self.find_spectrogram(song_data, sample_rate)
        return Sxx_dB

    def mix_spectrograms(self, file_path1, file_path2, slider_value):
        '''
        slider values: is the value of slider for file uploaded number 1
        It's maped from (0->1)
        '''
        spectrogram1= self.extract_spectrogram(file_path1)
        spectrogram2= self.extract_spectrogram(file_path2)
        mixed_spectrogram= (slider_value)*spectrogram1 + (1-slider_value)*spectrogram2
        return mixed_spectrogram




    #THIS IS WRITTEN TO BE EXECUTED ONCE
    def extract_and_save_75_spectrograms(self):
        #loop over folders  
        main_folder="D:\SBME 2026\Fifth term\DSP\Tasks\Task 5 Data"
        for subfolder_name in os.listdir(main_folder):
            subfolder_path = os.path.join(main_folder, subfolder_name)    
            # Check if it's a directory
            if os.path.isdir(subfolder_path):
                # Loop through each WAV file in the subfolder
                for file_name in os.listdir(subfolder_path):
                    if file_name.endswith('.wav'):  # Check for WAV files
                        file_path = os.path.join(subfolder_path, file_name)
                        sample_rate, song = wavfile.read(file_path)
                        duration=30
                        num_samples = duration * sample_rate
                        if len(song.shape) == 1:
                            song_data = song[:num_samples] 
                        elif len(song.shape) >1 :
                            song_data = song[:num_samples,0]
                        Sxx_dB= self.find_spectrogram(song_data, sample_rate)
                        self.save_spectrogram(Sxx_dB, file_name)
                    else:
                        print(f"{file_name} doesn't ends with wav")

    def save_spectrogram(self, spectrogram, name, output_folder_name):
        np.save(os.path.join(f"{output_folder_name}", f"{name}.npy"), spectrogram)