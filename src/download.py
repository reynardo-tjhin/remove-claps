from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import argparse

def download_youtube_mp3(name: str, yt_link: str) -> None:
    """
    Download a youtube audio only video.
    Automatically converted to mp3.
    The file can be seen in the main directory (not inside src).

    :param name: the name of the song to be exported in mp3
    :param yt_link: the youtube link
    """
    try:
        # download
        print(f"Downloading '{yt_link}' as '{name}.mp3'")
        yt = YouTube(yt_link)
        stream = yt.streams.get_by_itag(140)
        stream.download(filename=f'{name}.mp4')
    except (Exception):
        print("Error: the YouTube link is either invalid, incorrect or the video is private/deleted.")
        return None

    # convert from mp4 to mp3
    print("Converting from mp4 to mp3...")
    VIDEO_FILE_PATH = f"./{name}.mp4"
    AUDIO_FILE_PATH = f"./{name}.mp3"

    FILETOCONVERT = AudioFileClip(VIDEO_FILE_PATH)
    FILETOCONVERT.write_audiofile(AUDIO_FILE_PATH)
    FILETOCONVERT.close()

    # remove the mp4 file
    os.remove(f"{name}.mp4")

    return None

if (__name__ == "__main__"):
    
    parser = argparse.ArgumentParser(description='Download YouTube Audio Video in MP3')
    parser.add_argument('-d', '--download', 
                        action='store',
                        required=True,
                        nargs=1, 
                        type=str,
                        help='provide the link to download the video in MP3 format')
    parser.add_argument('-n', '--name', 
                        action='store',
                        required=True,
                        nargs=1, 
                        type=str,
                        help='provide the name of the downloaded MP3 audio')
    args = parser.parse_args()

    download_youtube_mp3(args.name[0], args.download[0])
