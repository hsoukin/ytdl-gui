#!/usr/bin/env python

from __future__ import unicode_literals
import sys
import youtube_dl


class LoggerClass(object):
    def debug(self, msg):
        print('DEBUG:', msg)
    
    def warning(self, msg):
        print('WARNING:', msg)
    
    def error(self, msg):
        print('ERROR:', msg)


def print_status(output_list=[]):
    def status_foo(dl):
        if dl["status"] == "finished":
            name = dl['filename']
            print(f"{name} was downloaded successfully.")
            output_list.append(str(name))

    return status_foo


def download(args, audio=True, ignore_errors=False):
    downloaded = []
    down_format = 'm4a' if audio else 'mp4'

    down_opts = {
        "format": down_format,
        "merge_output_format": down_format,
        "outtmpl": "%(title)s.%(ext)s",
        "writethumbnail": True,
        "ignoreerrors": ignore_errors,
        # "restrictfilenames": True,
        # "download_archive": f"download-list.txt",
        "postprocessors": [
            {"key": "FFmpegMetadata"},
        ],
        "progress_hooks": [print_status(output_list=downloaded)],
        "logger": LoggerClass(),
    }

    audio_opts = [
        {"key": "EmbedThumbnail"},
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": 'm4a',
        },
    ]

    if audio:
        down_opts['postprocessors'].extend(audio_opts)

    try:
        with youtube_dl.YoutubeDL(down_opts) as ydl:
            print(f'Downloading {args}...')
            ydl.download(args)
            print(downloaded)
            return downloaded
    except Exception as e:
        if __name__ != '__main__' and str(e) != '\'mp4\'':
            raise
            print(e)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_list = [arg for arg in sys.argv[1:]]
    else:
        print("Please paste in the URL to the videos you'd like to",
              "download, separated by spaces.")
        arg_list = input("").split(" ")
    download(arg_list)
    sys.exit(0)
