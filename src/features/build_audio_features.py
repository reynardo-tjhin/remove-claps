import librosa
import pandas as pd
import numpy as np
import os

# constants
FRAME_LENGTH = 2048
HOP_LENGTH = 512

# create a DataFrame to store the audio features in a CSV file later
df = pd.DataFrame({
    'audio_name': [],
    'rms': [],
    'zcr': [],
    'spectral_centroid':  [],
    'spectral_bandwidth': [],
    'spectral_flatness': [],
    'class': []
})

print("Building Audio Features for 'yes' class")

# loop through each audio in the "yes" category
for audio_name in os.listdir("../../data/yes"):
    
    # load the audio using librosa
    audio_path = "../../data/yes/" + audio_name
    audio, sr = librosa.load(audio_path)

    # calculate the features
    audio_rms = librosa.feature.rms(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_zcr = librosa.feature.zero_crossing_rate(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_spectral_flatness = librosa.feature.spectral_flatness(y=audio, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)
    
    # perform aggregation for Machine Learning
    audio_rms = np.mean(audio_rms)
    audio_zcr = np.mean(audio_zcr)
    audio_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_spectral_bandwidth = np.mean(audio_spectral_bandwidth)
    audio_spectral_flatness = np.mean(audio_spectral_flatness)

    # create a new array to be stored
    features = [
        audio_name,
        audio_rms,
        audio_zcr,
        audio_spectral_centroid,
        audio_spectral_bandwidth,
        audio_spectral_flatness,
        "yes"
    ]

    # add to the DataFrame
    df.loc[len(df)] = features



print("Building Audio Features for 'no' class")

# loop through each audio in the "no" category
for audio_name in os.listdir("../../data/no"):
    
    # load the audio using librosa
    audio_path = "../../data/no/" + audio_name
    audio, sr = librosa.load(audio_path)

    # calculate the features
    audio_rms = librosa.feature.rms(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_zcr = librosa.feature.zero_crossing_rate(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)
    audio_spectral_flatness = librosa.feature.spectral_flatness(y=audio, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)
    
    # perform aggregation for Machine Learning
    audio_rms = np.mean(audio_rms)
    audio_zcr = np.mean(audio_zcr)
    audio_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_spectral_bandwidth = np.mean(audio_spectral_bandwidth)
    audio_spectral_flatness = np.mean(audio_spectral_flatness)

    # create a new array to be stored
    features = [
        audio_name,
        audio_rms,
        audio_zcr,
        audio_spectral_centroid,
        audio_spectral_bandwidth,
        audio_spectral_flatness,
        "no"
    ]

    # add to the DataFrame
    df.loc[len(df)] = features



print("Exporting to csv")

# export to csv
df.to_csv("../../data/data.csv", index=False)
