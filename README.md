# Fingerprint-ShazamLikeApp

This project is designed to perform similarity searches and match audio files based on their acoustic fingerprints. The tool allows users to upload two audio files and adjust the mixing ratio of their spectrograms. By computing the unique fingerprint of each audio file and comparing it with precomputed hashes, this tool returns the most similar audio files from a predefined database. It is a great demonstration of digital signal processing, audio analysis, and similarity search techniques applied to sound files.

The application also enables the user to explore the impact of spectrogram mixing using a slider, offering a hands-on interaction with signal processing concepts such as feature extraction, hashing, and similarity computation.

---
## Video Demonstration

Here is a video demonstration of how the application works :


---

## Features

### **Audio File Upload**
- **File Selection**: Allows users to upload two audio files using an intuitive file browsing interface.

### **Spectrogram Extraction**
- **Spectrogram Generation**: For each uploaded audio file, the tool generates a spectrogram using signal processing techniques.
  - The spectrogram visualizes the frequency content of the audio over time.

### **Fingerprint Generation and Hashing**
- **Feature Extraction**: Extracts meaningful features from the spectrograms of the audio files.
  - Computes a unique audio fingerprint for each file using perceptual hashing.
  - Stores the fingerprints as precomputed hash values for later comparison.

### **Similarity Search**
- **Similarity Computation**: Compares the fingerprint of a newly uploaded file to precomputed fingerprints from a database of audio files.
  - Uses Hamming distance to compute the similarity between audio fingerprints.
  - Displays the top 10 most similar audio files with a similarity percentage.

### **Spectrogram Mixing**
- **Customizable Mixing**: Allows users to mix the spectrograms of two audio files by adjusting the mixing ratio via a slider.
  - The resulting mixed spectrogram can be used to generate a new fingerprint for similarity comparison.
  - Provides a real-time preview of how the spectrograms are blended.

### **Slider Controls**
- **Adjust Weight**: Users can control the mixing ratio of the two spectrograms using two sliders, which will adjust the strength of each file in the mixed spectrogram.
  - The weight of each file is automatically adjusted based on the slider values.

### **Progress Indicators**
- **Real-Time Feedback**: The application provides a progress bar during lengthy operations (e.g., similarity computation and mixing) to keep the user informed of the process status.
- **Cancellation Option**: Users can cancel ongoing operations if they wish to make new adjustments before the process is completed.

---

## Requirements

Before running the application, ensure you have the following dependencies installed:

- Python 3.x
- PyQt5
- numpy
- scipy
- scikit-learn
- pydub

## Usage
Clone the repo
```python
git clone https://github.com/JudyEssam/Fingerprint-ShazamLikeApp
```
Install the following libraries
```python
pip install numpy scipy pyqt5 scikit-learn pydub
```

## Contributors

- [Laila Khaled](https://github.com/LailaKhaled352)
- [Fatma Elsharkawy](https://github.com/FatmaElsharkawy)
- [Judy Essam](https://github.com/JudyEssam)
- [Hajar Ehab](https://github.com/HajarEhab)
