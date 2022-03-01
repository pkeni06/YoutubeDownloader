from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube, Playlist, Search
import os
import sys

dir = os.getcwd()


def progress_callback(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    current = ((filesize - bytes_remaining) / filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


def complete_callback(stream, file_handle):
    print("downloading finished")
    # progress bar stop call from GUI here


def downloadVideo(URL, i=1, j=1):
    try:
        yt = YouTube(URL)
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)

    except Exception as e:
        print(e, "url issue")

    stream = yt.streams.get_audio_only()

    print(i, " out of ", j, " : ", yt.title)

    try:
        convert(stream.download(output_path=dir))
    except Exception as e:
        print(e)


def DownloadVideoFromObject(videoObject):
    stream = videoObject.streams.get_audio_only()
    videoObject.register_on_progress_callback(progress_callback)
    videoObject.register_on_complete_callback(complete_callback)
    print(stream)
    try:
        convert(stream.download(output_path=dir))
    except Exception as e:
        print(e,"search error")



def downloadPlaylist(url):
    try:
        p = Playlist(url)

    except Exception as e:
        print(e, "Invalid URL")
        exit(0)
    i = 0
    try:
        for urls in p.video_urls:
            i = i + 1
            downloadVideo(urls, i, len(p.video_urls))
    except Exception as e:
        print(e, "Invalid URL")


def searchSong(name):
    s = Search(name)
    i = 0
    for song in s.results:
        i = i + 1
        print(i, " ", song.title)
    try:
        choice = int(input("Enter Choice: "))
    except Exception as e:
        print(e)

    try:
        DownloadVideoFromObject(s.results[choice - 1])
    except Exception as e:
        print(e)


def convert(path):
    audio = AudioFileClip(path)
    audio.write_audiofile(path[:-4]+".mp3")
    audio.close()
    os.remove(path)


if __name__ == "__main__":
    while True:
        print("1. Playlist\n"
              "2. Song\n"
              "3. Search\n"
              "4. Exit\n")

        i = int(input("Enter Choice: "))

        if i == 1:
            url = input("Enter Playlist URL: ")
            downloadPlaylist(url)

        if i == 2:
            url = input("Enter Playlist URL: ")
            downloadVideo(url)

        if i == 3:
            l = input("Enter Song name: ")
            searchSong(l)

        if i == 4:
            exit(0)
