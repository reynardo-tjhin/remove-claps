# Import Libraries
import os
import pandas as pd
from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment


def convertMP4toMP3(video_name="sample"):
    """
    A simple function that converts an mp4 video to mp3.

    Requires: MoviePy module.
    """
    video_name = video_name.replace(".mp4", "")

    VIDEO_FILE_PATH = "./audio/mp4/" + video_name + ".mp4"
    AUDIO_FILE_PATH = "./audio/mp3/" + video_name + ".mp3"

    FILETOCONVERT = AudioFileClip(VIDEO_FILE_PATH)
    FILETOCONVERT.write_audiofile(AUDIO_FILE_PATH)
    FILETOCONVERT.close()


def split(start: int, end: int, audio_name="/path/to/sample", audio_result_name="sample"):
    """
    Split and create a wav from the give start and end time of the audio segment.

    :param start: the starting time (in milliseconds)
    :param end: the ending time (in milliseconds)
    :param audio_name: the path to the audio
    :param audio_result: the name of the audio exported

    Requires: Pydub module.
    Dependencies: ffmpeg (using sudo apt install) and ffprobe (using pip3 install).
    """
    if (end < start):
        print("Error: End duration is earlier than start duration")
        return

    # write the audio file path
    AUDIO_FILE_PATH = "." + audio_name + ".mp3"

    # create a sound object using pydub module
    sound = AudioSegment.from_file(AUDIO_FILE_PATH, format="mp3")

    # grab the first five seconds of the audio
    first_seconds = sound[start:end]

    # simple export to 2 different file formats: wav and mp3
    # first_five_seconds.export("test.mp3", format="mp3")
    first_seconds.export(f"{audio_result_name}.wav", format="wav")


if (__name__ == "__main__"):

    # get to the main directory
    os.chdir("../")
    os.chdir("../")

    # get the youtube links
    links_data = pd.read_csv("music_links.csv")
    yt_links = links_data.iloc[:, 1].to_list()

    # check if the directory "audio" exists
    if (not os.path.exists("./audio")):
        os.makedirs("audio")
        os.makedirs("audio/mp4")
        os.makedirs("audio/mp3")
    
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
        if (not os.path.exists("audio/mp3/" + name + ".mp3")):
            # converting mp4 to mp3
            convertMP4toMP3(video_name=name)
        else:
            print(f"{name} found... Skipping...")

    print()

    # check if the directory "data" exists
    if (not os.path.exists("./data")):
        os.makedirs("data")
        os.makedirs("data/yes")
        os.makedirs("data/no")

    # create the classes of yes and no
    data = pd.read_csv("dataset.csv")

    # duration based on exploration.ipynb
    duration = 1800 # in milliseconds

    # making a "yes" class
    i = 0
    j = 0
    for audio in data.loc[:, 'audio_name']:

        print(f"splitting {audio}.mp3")

        # clapping before performance
        clap_start_time = data.loc[i, 'clap_start'] * 1000
        clap_end_time = data.loc[i, 'clap_end'] * 1000
        while (clap_start_time + duration < clap_end_time):

            # print(f"{j}.wav is from {audio}.mp3")

            if (os.path.exists("data/yes/" + f"{j}.wav")):
                clap_start_time += duration
                j += 1
                continue

            # split and export the resulting audio to current directory
            split(clap_start_time, clap_start_time+duration, audio_name=f"/audio/mp3/{audio}", audio_result_name=str(j))
            
            # move to the next start time
            clap_start_time += duration

            # move to the data
            os.rename(f"./{j}.wav", f"./data/yes/{j}.wav")

            # for data audio name
            j += 1

        # clapping after performance
        end_clap_time = data.loc[i, 'end_clap_start'] * 1000
        audio_end_time = data.loc[i, 'end_clap_end'] * 1000
        while (end_clap_time + duration < audio_end_time):

            # print(f"{j}.wav is from {audio}.mp3")

            if (os.path.exists("data/yes/" + f"{j}.wav")):
                end_clap_time += duration
                j += 1
                continue

            # split and export the resulting audio to current directory
            split(end_clap_time, end_clap_time+duration, audio_name=f"/audio/mp3/{audio}", audio_result_name=str(j))
            
            # move to the next start time
            end_clap_time += duration

            # move to the data
            os.rename(f"./{j}.wav", f"./data/yes/{j}.wav")

            # for data audio name
            j += 1

        # loop through each audio
        i += 1


    print()


    # making a "no" class
    i = 0
    for audio in data.loc[:, 'audio_name']:

        # the silence before performing
        print(f"splitting {audio}.mp3")
        clap_end_time = data.loc[i, 'clap_end'] * 1000
        music_start_time = data.loc[i, 'music_start'] * 1000
        while (clap_end_time + duration < music_start_time):

            if (os.path.exists("data/yes/" + f"{j}.wav")):
                clap_end_time += duration
                j += 1
                continue

            # split and export the resulting audio to current directory
            split(clap_end_time, clap_end_time+duration, audio_name=f"/audio/mp3/{audio}", audio_result_name=str(j))
            
            # move to the next start time
            clap_end_time += duration

            # move to the data
            os.rename(f"./{j}.wav", f"./data/no/{j}.wav")

            # for data audio name
            j += 1

        # to increase more "no" class data
        another_duration = 20 # seconds
        end_clap_time = data.loc[i, 'end_clap_start'] * 1000
        music_coming_to_an_end_time = end_clap_time - (20 * 1000)
        while (music_coming_to_an_end_time + duration < end_clap_time):

            if (os.path.exists("data/yes/" + f"{j}.wav")):
                music_coming_to_an_end_time += duration
                j += 1
                continue

            # split and export the resulting audio to current directory
            split(music_coming_to_an_end_time, music_coming_to_an_end_time+duration, audio_name=f"/audio/mp3/{audio}", audio_result_name=str(j))
            
            # move to the next start time
            music_coming_to_an_end_time += duration

            # move to the data
            os.rename(f"./{j}.wav", f"./data/no/{j}.wav")

            # for data audio name
            j += 1

        # loop through each audio
        i += 1
