# download_youtube_playlist
A python3 script for easily downloading and archiving entire YouTube playlists from the console. Downloads audio and video in highest quality along with thumbnail and english captions when available. Uses pytube, colorful and ffmpeg.

This was created to aid in backing-up and archiving data from youtube.

This was originally made so that I could conviniently and efficiently make high quality backups of my kpop playlists with subtitles and important metadata.

It also really helps that this is being done in a simple script for Linux. Anyone can read and modify this. No need to rely on some third party site or app and hope for the best.

# Installation
```shell
sudo ./install.sh
```

# Usage
```download_youtube_playlist``` and you will be prompted for a url (ex. https://www.youtube.com/playlist?list=OLAK5uy_nK6if5UyWpbIza-ZRjfqayJ1G-nn5RJZs)

or

```shell
download_youtube_playlist https://www.youtube.com/playlist?list=OLAK5uy_nK6if5UyWpbIza-ZRjfqayJ1G-nn5RJZs
```

# Implementation
A new directory is created for each playlist and subdirectories are created for each video.

Playlist directories are named after the title of the playlist. Video subdirectories are named after the title of the video.

The directories names are corrected or 'escaped()' and the '/' characters are changed to '|'.

Pytube recommends that audio and video streams are downloaded seperately. This is what I'm doing and at the end I use ffmpeg to merge the two files together before deleting the artifacts.

The way I select the streams is really simple: whichever two streams at the largest (audio and video) are the winners.


