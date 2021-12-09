#!/usr/bin/python3

import pytube
from pytube import Playlist
from pytube import YouTube

import colorful as cf

import os
import sys
import urllib.request
from shlex import quote

import shutil

DEBUG = False

def printinfo(string):
    print(cf.lightBlue(string))
    

def printlog(string):
    print(cf.gray(string))


def printwarn(string):
    print(cf.lightYellow(string))


def printerror(string):
    print(cf.lightCoral(string))


def printdebug(string):
    print(cf.lightGreen(string))


def escape(string):
    return string.translate(str.maketrans({
        '/': '|'
    }))


def decide(yt):
    prev_size = {
        'video': 0,
        'audio': 0
    }
    ret = {
        'video': None,
        'audio': None
    }

    for stream in yt.streams.filter(only_video=True):
        if(stream.filesize > prev_size['video']):
            prev_size['video'] = stream.filesize
            ret['video'] = stream

    for stream in yt.streams.filter(only_audio=True):
        if(stream.filesize > prev_size['audio']):
            prev_size['audio'] = stream.filesize
            ret['audio'] = stream

    return ret


def on_progress(chunk, file_handle, bytes_remaining):
    print("remaining: " + str( round(bytes_remaining / float(1000*1000), 1) ) +"MB" )


def download_video(url):
    yt = None
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except pytube.exceptions.VideoPrivate:
        printerror("Video {url} is private - skipping")
        return

    title = escape(yt.title)
    printlog("Downloading video")
    printinfo(yt.title)
    printlog("{0} (corrected)".format(title))

    if(os.path.exists(title+"/lock")):
        printerror("{title} is in an invalid state as lock file is present. This likely means that the download process was previously interrupted. Directory will be rewritten.".format(title=title))

        shutil.rmtree(title)

    if(os.path.exists(title)):
        printwarn("Directory already exists! - Skipping video")
        return

    if(DEBUG):
        printdebug("########## Stream Info #########")
        for stream in yt.streams:
            printdebug(str(stream) + " " + str(stream.filesize))
        printdebug("################################")
        printdebug(stream)
        printdebug(stream.filesize)
        printdebug("################################")

    os.mkdir(title)

    #os.system("touch {0}/lock".format(title))
    with open(title+"/lock", 'a'):  # Create file if does not exist
        pass

    url_file = open("{0}/url".format(title), 'w')
    url_file.write(url)
    url_file.close()

    printlog("Downloading thumbnail")

    urllib.request.urlretrieve(yt.thumbnail_url, title + '/thumbnail.ico')

    printlog("Downloading captions")
    try:
        captions = yt.captions['en']
        if (type(captions) == 'list' or type(captions) == 'tuple'):
            for caption in captions:
                caption.download(title=caption.name + ".xml",
                                 srt=False, output_path=title)
        else:
            captions.download(title=captions.name + ".xml",
                              srt=False, output_path=title)

    except:
        printerror("There was an error handling captions for this video. This likely means that there are no english captions available. Captions downloading will be skipped.")

    s = decide(yt)
    if(DEBUG):
        printdebug('###### streams ######')
        printdebug(s)
        printdebug('###### ####### ######')

    v = s['video']
    a = s['audio']

    vf = v.get_file_path("video", title)
    af = a.get_file_path("audio", title)

    extension = v.subtype

    if(DEBUG):
        printdebug('#######')
        printdebug(vf)
        printdebug(af)
        printdebug(extension)
        printdebug('#######')

        printlog("Downloading video")
    v.download(title, "video", None, True)
    printlog("Downloading audio")
    a.download(title, "audio", None, True)

    printlog("Merging audio and video")
    os.system("ffmpeg -i {vf} -i {af} -c:v copy {title}/main.{ext}".format(vf=quote(vf), af=quote(af), ext=extension,
                                                                           title=quote(title)))

    os.remove(vf)
    # os.remove(af)

    os.remove(title+"/lock")


'''
i = 0
for stream in yt.streams:
    d = yt.title+"/"+str(i)
    os.mkdir(d)
    stream.download(d, stream.default_filename, None, True)
    i += 1
'''

plurl = ""
if(len(sys.argv) > 1):
    plurl = sys.argv[1]
else:
    plurl = input(cf.orange("Please provide a playlist URL to download: "))

playlist = Playlist(plurl)
title = escape(playlist.title)
count = len(playlist.video_urls)
printinfo("############ {title}             ############".format(
    title=playlist.title))
printlog("############ {title} (corrected) ############".format(title=title))
printlog('Number of videos in playlist: %s' % count)

# playlist.download_all()

try:
    os.mkdir(escape(title))
except:
    printwarn("Playlist directory seems to already exist")

printdebug("change dir: " + title)
os.chdir(title)
i = 1
for url in playlist.video_urls:
    printlog("Video {0} of {1}".format(i, count))
    download_video(url)
    i += 1
