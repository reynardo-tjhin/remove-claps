from moviepy.editor import *
from pydub import AudioSegment
import os

def convertMP4toMP3(video_name="sample"):
    """
    A simple function that converts an mp4 video to mp3.

    Requires: MoviePy module.
    """
    video_name = video_name.strip(".mp4")

    VIDEO_FILE_PATH = "./audio/mp4/" + video_name + ".mp4"
    AUDIO_FILE_PATH = "./audio/mp3/" + video_name + ".mp3"

    FILETOCONVERT = AudioFileClip(VIDEO_FILE_PATH)
    FILETOCONVERT.write_audiofile(AUDIO_FILE_PATH)
    FILETOCONVERT.close()


def split(start: int, end: int, audio_name="sample", audio_result_name="sample"):
    """
    Split and create an mp3 from the start and end time of the audio segment.

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
    first_seconds.export("test.wav", format="wav")


# main
if (__name__ == "__main__"):

    end_time = 50

    print(f"Converting MP4 to MP3 and getting only the first {end_time} seconds of the audio")

    for name in os.listdir("audio/mp4"):

        name = name.replace(".mp4", "")
        if (not os.path.exists("audio/mp3/" + name + ".mp3")):

            # converting mp4 to mp3
            convertMP4toMP3(video_name=name)

        # testing splitting audio
        # split(0, end_time * 1000, audio_name=name, audio_result_name=name)

        else:
            print(f"{name} found... Skipping...")

