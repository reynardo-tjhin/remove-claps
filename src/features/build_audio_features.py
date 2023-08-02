import librosa
import pandas as pd
import numpy as np
import os

# constants
FRAME_LENGTH = 1024
HOP_LENGTH = 512

# create a DataFrame to store the audio features in a CSV file later
df = pd.DataFrame({
    'audio_name': [],
    'mean_rms': [],
    'std_rms': [],
    'mean_zcr': [],
    'mean_spectral_centroid':  [],
    'std_spectral_bandwidth': [],
    'mean_spectral_flatness': [],
    'mean_spectral_rolloff': [],
    'class': []
})

print("Building Audio Features for 'yes' class")

# loop through each audio in the "yes" category
for audio_name in os.listdir("../../data/yes"):
    
    # load the audio using librosa
    audio_path = "../../data/yes/" + audio_name
    audio, sr = librosa.load(audio_path)

    # calculate the features
    audio_rms = librosa.feature.rms(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_zcr = librosa.feature.zero_crossing_rate(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_flatness = librosa.feature.spectral_flatness(y=audio, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]

    # perform aggregation for Machine Learning
    audio_mean_rms = np.mean(audio_rms)
    audio_std_rms = np.std(audio_rms)
    audio_mean_zcr = np.mean(audio_zcr)
    audio_mean_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_std_spectral_bandwidth = np.std(audio_spectral_bandwidth)
    audio_mean_spectral_flatness = np.mean(audio_spectral_flatness)
    audio_mean_spectral_rolloff = np.mean(audio_spectral_rolloff)

    # create a new array to be stored
    features = [
        audio_name,
        audio_mean_rms,
        audio_std_rms,
        audio_mean_zcr,
        audio_mean_spectral_centroid,
        audio_std_spectral_bandwidth,
        audio_mean_spectral_flatness,
        audio_mean_spectral_rolloff,
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
    audio_rms = librosa.feature.rms(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_zcr = librosa.feature.zero_crossing_rate(y=audio, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_flatness = librosa.feature.spectral_flatness(y=audio, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]
    audio_spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, n_fft=FRAME_LENGTH, hop_length=HOP_LENGTH)[0]

    # perform aggregation for Machine Learning
    audio_mean_rms = np.mean(audio_rms)
    audio_std_rms = np.std(audio_rms)
    audio_mean_zcr = np.mean(audio_zcr)
    audio_mean_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_std_spectral_bandwidth = np.std(audio_spectral_bandwidth)
    audio_mean_spectral_flatness = np.mean(audio_spectral_flatness)
    audio_mean_spectral_rolloff = np.mean(audio_spectral_rolloff)

    # create a new array to be stored
    features = [
        audio_name,
        audio_mean_rms,
        audio_std_rms,
        audio_mean_zcr,
        audio_mean_spectral_centroid,
        audio_std_spectral_bandwidth,
        audio_mean_spectral_flatness,
        audio_mean_spectral_rolloff,
        "no"
    ]

    # add to the DataFrame
    df.loc[len(df)] = features




print("Exporting to csv")

# export to csv
df.to_csv("../../data/data.csv", index=False)
