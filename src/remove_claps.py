import pickle
import os
import librosa
import numpy as np
import pandas as pd
import math
import argparse
from pydub import AudioSegment
from sklearn.preprocessing import StandardScaler

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

def remove_claps(audio_file_path: str, step=0.05, duration=1.8, model_path="../models/MLPClassifier.pickle") -> list:
    """
    10 models that can be used:
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

    :param audio_file_path: the path to the mp3 audio
    :param step: to clean the claps in order not to be in multiples of duration (in seconds)
    :param duration: duration of the clap based on training (in seconds)
    :param model_path: the path to the model stored in models directory

    :result a list of clapping start time and clapping end times (in tuples)
    """

    # get the data
    dataset = pd.read_csv("./data-features/data.csv")
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

    clapping_starts = []
    clapping_ends = []
    is_clapping = False

    # main loop
    is_not_finished = True
    while (is_not_finished):

        if (start_time + duration > end_time):
            start_time = end_time - duration
            is_not_finished = False

        # split audio
        sound = audio[start_time*1000:(start_time + duration)*1000]
        sound.export("test.wav", format="wav")
        features = build_audio_features("./test.wav")
        features = sc.transform(features)

        # get prediction
        prediction = model.predict(features)

        # print the output
        print("%.2f to %.2f -> %s" % (start_time, start_time+duration, str(prediction)))

        if (prediction == 1):

            # the first of block of clapping sound
            if (is_clapping == False):

                # do some cleaning at the start of the sound
                # to ensure that the end of music does not cut abruptly
                if (not math.isclose(start_time, 0.0)):

                    new_start = start_time - step
                    while (prediction != 0):

                        if (new_start < 0 or math.isclose(new_start, 0.0)):
                            new_start = 0.0
                            break

                        sound = audio[new_start*1000:(new_start + duration)*1000]
                        sound.export("test.wav", format="wav")
                        features = build_audio_features("test.wav")
                        features = sc.transform(features)
                        prediction = model.predict(features)
                        new_start -= step
                    
                    clapping_starts.append(new_start)
                
                else:
                    clapping_starts.append(start_time)
            
            # clapping sound extends until the end of the audio
            if (math.isclose(start_time + duration, end_time)):
                clapping_ends.append(end_time)
            
            is_clapping = True

        else:
            # the first non-clapping sound is obtained
            # the first block of sound RIGHT after clapping ends
            if (is_clapping):

                # do some cleaning - trimming until the prediction is 1
                new_start = start_time - step
                while (prediction != 1):

                    if (new_start < 0 or math.isclose(new_start, 0.0)):
                        new_start = 0.0
                        break

                    sound = audio[new_start*1000:(new_start + duration)*1000]
                    sound.export("test.wav", format="wav")
                    features = build_audio_features("test.wav")
                    features = sc.transform(features)
                    prediction = model.predict(features)
                    new_start -= step

                clapping_ends.append(new_start)
            
            is_clapping = False
        
        # update start_time
        start_time += duration

    # remove the temporary file
    os.remove("./test.wav")

    return tuple(zip(clapping_starts, clapping_ends))

def export_result(clapping_list: list, audio_file_path: str) -> None:
    
    i = 0
    while (i < len(clapping_list) - 1):
        
        # get the start of music and end of music times
        start_of_music = clapping_list[i][1]
        end_of_music = clapping_list[i + 1][0]

        # trim
        audio = AudioSegment.from_file(audio_file_path, format="mp3")
        trimmed_audio = audio[int(start_of_music * 1000):int(end_of_music * 1000)]
        trimmed_audio.export(f"result{i}.mp3", format="mp3")
        
        i += 1


if (__name__ == "__main__"):

    parser = argparse.ArgumentParser(description='Remove claps from MP3 file')
    parser.add_argument('-f', '--file',
                        action='store',
                        required=True,
                        nargs=1,
                        type=str,
                        help='provide the name of the MP3 file in the current directory')
    args = parser.parse_args()

    audio_file_path = args.file[0] + ".mp3"
    model_file_path = "./models/MLPClassifier.pickle"

    print("Finding the clapping time(s)...")
    result = remove_claps(audio_file_path=audio_file_path, model_path=model_file_path)
    print("Done!")

    print("Trimming Starts...")
    export_result(clapping_list=result, audio_file_path=audio_file_path)
    print("Done!")

