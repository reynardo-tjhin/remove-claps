from moviepy import *
from youtube_dl.utils import std_headers

import os
import argparse
import youtube_dl

def download_youtube_mp3(name: str, yt_link: str) -> None:
    """
    Download a youtube audio only video.
    Automatically converted to mp3.
    The file can be seen in the main directory (not inside src).

    :param name: the name of the song to be exported in mp3
    :param yt_link: the youtube link
    """
    print(f"Downloading from: {yt_link}")
    print(f"Saving as: {name}.mp3")

    # work around to prevent bot error
    std_headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # some configurations that can be used to download yt video
    ydl_opts = {
        'verbose': True,
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        
        # get the filename
        info = ydl.extract_info(yt_link, download=False)
        filename = ydl.prepare_filename(info)
        extension = info.get("ext")

        # download the video as mp4
        print(f"Downloading from '{yt_link}' as '{filename}'")
        ydl.download([yt_link])

    # filename = "Rachmaninov Piano Concerto No  2, Evgeny Kissin HD-l4zkc7KEvYM.mp4"

    if (filename == "" or filename == None):
        print("Error: reading filename")
        return

    if (not os.path.exists(os.path.join(os.path.curdir, filename))):
        print("Error: download unsuccessful")
        return

    # rename to temp.mp4
    old = os.path.join(os.path.curdir, f"{filename}")
    new = os.path.join(os.path.curdir, f"temp.{extension}")
    if not os.path.exists(new):
        os.rename(old, new)

    # convert mp4 to mp3
    print("Converting from mp4 to mp3...")
    FILETOCONVERT = AudioFileClip(f"temp.{extension}")
    FILETOCONVERT.write_audiofile(f"{name}.mp3")
    FILETOCONVERT.close()

    # remove the mp4 file if exists
    if (os.path.exists(os.path.join(os.path.curdir, f"temp.{extension}"))):
        os.remove(f"temp.{extension}")

    return

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
