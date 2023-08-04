import pickle
import os
import librosa
import numpy as np
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
    FRAME_LENGTH = 1024
    HOP_LENGTH = 512

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
    audio_mean_spectral_centroid = np.mean(audio_spectral_centroid)
    audio_std_spectral_bandwidth = np.std(audio_spectral_bandwidth)
    audio_mean_spectral_flatness = np.mean(audio_spectral_flatness)
    audio_mean_spectral_rolloff = np.mean(audio_spectral_rolloff)

    # create an np array features
    features = np.array([
        audio_mean_rms,
        audio_std_rms,
        audio_mean_zcr,
        audio_mean_spectral_centroid,
        audio_std_spectral_bandwidth,
        audio_mean_spectral_flatness,
        audio_mean_spectral_rolloff,
    ])

    return features

def split_audio(start: int, end: int, audio_file_path: str) -> None:
    """
    Split the audio from start to end.

    :param start: the starting time of the audio
    :param end: the ending time of the audio
    :param audio_file_path: the path of the audio to be cut
    """
    audio = AudioSegment.from_file(audio_file_path, format="mp3")
    sound = audio[start*1000:end*1000]
    sound.export("test.wav", format="wav")

    return None

def load_model(model_file_path: str):
    """
    :param model_file_path: a pickle file path
    :return a model that was saved
    """
    with open(model_file_path, 'rb') as model_file:
        return pickle.load(model_file)

def remove_claps(audio_file_path: str, duration=1.8, model_path="../models/MLPClassifier.pickle"):
    
    # remove claps in the opening
    
    # split the audio
    split_audio(0, 1.8, audio_file_path)

    # build the features
    features = np.reshape(build_audio_features("test.wav"), (1, 7))

    sc = StandardScaler()
    sc.fit_transform(features)

    # get the model
    model = load_model(model_path)

    print(model.predict(features))


if (__name__ == "__main__"):
    
    remove_claps(audio_file_path="../sample.mp3")


