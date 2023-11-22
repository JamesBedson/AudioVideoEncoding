import subprocess
import os

''' 4) Create a new script which will download subtitles, integrate them and output a video with
printed subtitles (this means, it will form part of the video track)'''

# Approach 1 --> Did not work
'''Create a new script which will download subtitles, integrate them and output a video with
printed subtitles (this means, it will form part of the video track) '''

'''
from subliminal import download_best_subtitles, save_subtitles, scan_videos
def download_subtitles(video_path: str, language: str = "en") -> None:
    
    videos      = scan_videos(video_path)
    
    print("Downloading Subtitles...")
    subtitles   = download_best_subtitles(videos, {language})
    
    print(subtitles)
    for video, subs in subtitles.items():
        save_subtitles(video, subs)
'''

# Approach 2 --> Did not work
'''
from pytube import YouTube
def download_subtitles(youtube_url, language = "en") -> None:
    
    yt_video    = YouTube(youtube_url)
    tracks      = yt_video.caption_tracks

    print(tracks)

    selected_track = None
    for track in tracks:
        if track.code == language:
            selected_track = track
            break
    
    if selected_track:
        subtitles = selected_track.generate_srt_captions()
        with open('subtitles.srt', 'w', encoding='utf-8') as file:
            file.write(subtitles)
        print(f'Subtitles downloaded successfully to subtitles.srt')
    
    else:
        print(f'No subtitles found for language code {language}')
'''

# Approach 3 --> Did not work
'''
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def download_subtitles(youtube_url, language="en") -> None:
    
    video_id = parse_qs(urlparse(youtube_url).query)['v'][0]

    try:
        transcript              = YouTubeTranscriptApi.get_transcript(video_id)
        selected_transcripts    = [entry['text'] for entry in transcript if entry.get('language') == language]

        if selected_transcripts:
            subtitles = '\n'.join(selected_transcripts)

            with open('subtitles.srt', 'w', encoding='utf-8') as file:
                file.write(subtitles)

            print(f'Subtitles downloaded successfully to subtitles.srt')
        else:
            print(f'No subtitles found for language code {language}')

    except Exception as e:
        print(f'An error occurred: {e}')
'''

import yt_dlp
def download_subtitles(youtube_url, file_name, language='en') -> None:
    
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [language],
        'skip_download': True,
        'outtmpl': file_name,
        'verbose': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])
            print(f'Subtitles downloaded successfully to {file_name}.en.vtt')
        except Exception as e:
            print(f'An error occurred: {e}')


import webvtt
import os
def convert_vtt_to_srt(vtt_file, srt_file) -> None:
    vtt = webvtt.read(vtt_file)
    srt_content = ""

    for i, caption in enumerate(vtt):                               #type: ignore
        start = caption.start
        end = caption.end
        text = caption.text.replace('\n', ' ')
        srt_content += f"{i + 1}\n{start} --> {end}\n{text}\n\n"

    with open(srt_file, 'w', encoding='utf-8') as srt_output:
        srt_output.write(srt_content)
    os.remove(vtt_file)


def integrate_subtitles(in_fp: str, subs_fp: str) -> None:
    
    cmd = ["ffmpeg", 
           "-i",
            in_fp, 
            "-vf",
            f"subtitles={subs_fp}",
            in_fp.split(".")[0] + "_subs.mp4"]
    
    subprocess.run(cmd)