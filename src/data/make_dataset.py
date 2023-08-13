# Import Libraries
import os
import glob
import pandas as pd
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment

def convertMP4toWAV(video_name="sample"):
    """
    A simple function that converts an mp4 video to wav.

    Requires: MoviePy module.
    """
    video_name = video_name.replace(".mp4", "")

    VIDEO_FILE_PATH = "./audio/mp4/" + video_name + ".mp4"
    AUDIO_FILE_PATH = "./audio/wav/" + video_name + ".wav"

    FILETOCONVERT = AudioFileClip(VIDEO_FILE_PATH)
    FILETOCONVERT.write_audiofile(AUDIO_FILE_PATH)
    FILETOCONVERT.close()

if (__name__ == "__main__"):

    # get to the main directory
    os.chdir("../")
    os.chdir("../")

    # get the youtube links
    links_data = pd.read_csv("./csv/music_links.csv")
    yt_links = links_data.iloc[:, 1].to_list()

    # check if the directory "audio" exists
    if (not os.path.exists("./audio")):
        os.makedirs("audio")
        os.makedirs("audio/mp4")
        os.makedirs("audio/wav")
    
    # download the audios based on the youtube linke
    i = 0
    for yt_link in yt_links:

        if (not os.path.exists(f"audio/mp4/audio{i}.mp4")):
            # create the YouTube object
            yt = YouTube(yt_link)

            print("Downloading " + "'" + yt.title + "'")
            stream = yt.streams.get_by_itag(140)
            stream.download(filename=f'audio{i}.mp4')
            print("Download Completed!")

            # move the downloaded audio to audio/mp4
            os.rename(f"./audio{i}.mp4", f"./audio/mp4/audio{i}.mp4")
            print()
        
        else:
            print(f"audio{i}.mp4 has already existed")

        i += 1

    print()

    # convert the audios to MP3 format
    for name in os.listdir("audio/mp4"):
        name = name.replace(".mp4", "")
        if (not os.path.exists("audio/wav/" + name + ".wav")):
            # converting mp4 to wav
            convertMP4toWAV(video_name=name)
        else:
            print(f"{name} found... Skipping...")

    print()

    # check if the directory "data" exists
    if (not os.path.exists("./data")):
        os.makedirs("data")
        os.makedirs("data/yes")
        os.makedirs("data/no")

    # create the classes of yes and no
    data = pd.read_csv("./csv/new_dataset.csv")

    # duration based on exploration.ipynb
    duration = 1.8 # in seconds

    i = 0

    print("Making 'yes' class data")
    # make 'yes' class data
    for row in range(data.shape[0]):

        audio_file_name = data.iloc[row, 0]
        start_time = data.iloc[row, 1]
        end_time = data.iloc[row, 2]

        print(f"Splitting Audio File Name: {audio_file_name}")

        audio = AudioSegment.from_file(f"./audio/wav/{audio_file_name}.wav", format="wav")
        is_not_finished = True
        while (is_not_finished):

            if (start_time + duration > end_time):
                start_time = end_time - duration
                is_not_finished = False

            cut_audio = audio[start_time * 1000:(start_time + duration) * 1000]
            cut_audio.export(f"{i}.wav", format="wav")

            start_time += duration        
            i += 1

    for file in glob.glob("*.wav"):
        os.rename(file, "./data/yes/" + file)

    print("Making 'no' class data")
    # make 'no' class data
    NUMBER_OF_WAV_FILES = len([name for name in os.listdir("./audio/wav") if os.path.isfile("./audio/wav/" + name)])
    for audio_id in range(NUMBER_OF_WAV_FILES):

        print(f"Splitting Audio File Name: audio{audio_id}")

        cut_data = data.loc[data['audio_name'] == f'audio{audio_id}']
        to_train = cut_data.iloc[:, 4].values[0]
        if (to_train == 0): continue

        audio = AudioSegment.from_file(f"./audio/wav/audio{audio_id}.wav", format="wav")
        for row in range(cut_data.shape[0] - 1):

            start_time = cut_data.iloc[row, 2]
            end_time = cut_data.iloc[row + 1, 1]
            is_not_finished = True
            while (is_not_finished):

                if (start_time + duration > end_time):
                    start_time = end_time - duration
                    is_not_finished = False

                cut_audio = audio[start_time * 1000:(start_time + duration) * 1000]
                cut_audio.export(f"{i}.wav", format="wav")

                start_time += duration        
                i += 1

    # move files
    for file in glob.glob("*.wav"):
        os.rename(file, "./data/no/" + file)
