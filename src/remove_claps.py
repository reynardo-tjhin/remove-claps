import pickle
import os
import librosa
import numpy as np
import pandas as pd
from pytube import YouTube
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from sklearn.preprocessing import StandardScaler

def download_youtube_mp3(name: str, yt_link: str) -> None:
    """
    Download a youtube audio only video.
    Automatically converted to mp3.
    The file can be seen in the main directory (not inside src).

    :param name: the name of the song to be exported in mp3
    :param yt_link: the youtube link
    """
    # download
    print("Downloading...")
    yt = YouTube(yt_link)
    stream = yt.streams.get_by_itag(140)
    stream.download(filename=f'{name}.mp4')

    # convert from mp4 to mp3
    print("Converting from mp4 to mp3...")
    VIDEO_FILE_PATH = f"./{name}.mp4"
    AUDIO_FILE_PATH = f"./{name}.mp3"

    FILETOCONVERT = AudioFileClip(VIDEO_FILE_PATH)
    FILETOCONVERT.write_audiofile(AUDIO_FILE_PATH)
    FILETOCONVERT.close()

    # remove the mp4 file
    os.remove(f"{name}.mp4")

    # move file to main directory
    os.rename(f"./{name}.mp3", f"../{name}.mp3")

    return None

def build_audio_features(audio_file_path: str) -> np.ndarray:
    """
    Build Audio Features using Librosa library.

    :param audio_file_path: a string to the .wav file
    :return an np array with its numerical features
    """

    # constants
    FRAME_LENGTH = 512
    HOP_LENGTH = 128

    # audio is in .wav file format
    # load the audio
    audio, sr = librosa.load(audio_file_path)

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
    audio_std_zcr = np.mean(audio_zcr)
    audio_mean_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_std_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_mean_spectral_bandwidth = np.std(audio_spectral_bandwidth)
    audio_std_spectral_bandwidth = np.std(audio_spectral_bandwidth)
    audio_mean_spectral_flatness = np.mean(audio_spectral_flatness)
    audio_std_spectral_flatness = np.mean(audio_spectral_flatness)
    audio_mean_spectral_rolloff = np.mean(audio_spectral_rolloff)
    audio_std_spectral_rolloff = np.mean(audio_spectral_rolloff)

    # create an np array features
    features = np.array([[
        audio_mean_rms,
        audio_std_rms,
        audio_mean_zcr,
        audio_std_zcr,
        audio_mean_spectral_centroid,
        audio_std_spectral_centroid,
        audio_mean_spectral_bandwidth,
        audio_std_spectral_bandwidth,
        audio_mean_spectral_flatness,
        audio_std_spectral_flatness,
        audio_mean_spectral_rolloff,
        audio_std_spectral_rolloff
    ]])

    return features

def remove_claps(audio_file_path: str, duration=1.8, model_path="../models/MLPClassifier.pickle"):
    """
    models:
    1. SVC
    2. ExtraTreesClassifier
    3. LinearDiscriminantAnalysis
    4. DecisionTreeClassifier
    5. KNeighborsClassifier
    6. RandomForestClassifier
    7. MLPClassifier
    8. AdaBoostClassifier
    9. NuSVC
    10. GaussianNB
    11. QuadraticDiscriminantAnalysis
    """

    # get the data
    dataset = pd.read_csv("../data/data.csv")
    X = dataset.iloc[:, 1:-1].values # independent variables: the features

    # perform feature scaling
    sc = StandardScaler()
    X = sc.fit_transform(X)
    
    # get the audio
    audio = AudioSegment.from_file(audio_file_path, format="mp3")
    start_time = 0
    end_time = len(audio) / 1000 # in seconds

    # get the model
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    i = 0

    # loop
    while (start_time + duration < end_time):

        # split audio
        sound = audio[start_time*1000:(start_time + duration)*1000]
        sound.export("test.wav", format="wav")

        # build the features
        features = build_audio_features("test.wav")

        # normalise the features
        features = sc.transform(features)

        # get prediction
        prediction = model.predict(features)

        # print the output
        print("%.2f to %.2f -> %s" % (start_time, start_time+duration, str(prediction)))

        # update start_time
        start_time += duration

    # remove the temporary file
    os.remove("./test.wav")



if (__name__ == "__main__"):
    
    audio_file_path = "../sample.mp3"
    model_file_path = "../models/MLPClassifier.pickle"

    remove_claps(audio_file_path=audio_file_path, model_path=model_file_path)


