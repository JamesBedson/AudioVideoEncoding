'''Create a python script which converts this video
into a .mp2 video file, and is able to parse the
‘ffmpeg –i BBB.mp2’ file and save the video info'''

import subprocess
import utils as utl
import re

def convert_to_mp2(video_path_in: str) -> None:
    video_out   = utl.parse_extension(video_path_in)[0] + ".mp2"
    cmd         = ["ffmpeg", "-i", video_path_in, "-c:a", "mp2", video_out]
    
    subprocess.run(cmd)

def get_info_from_video(video_path: str) -> subprocess.CompletedProcess[str]:
    cmd = ["ffmpeg", "-i", video_path]

    return subprocess.run(cmd,
                          capture_output = True,
                          text = True)
    

def parse_video_information(mp2_information: subprocess.CompletedProcess[str]) -> dict:
    info            = str(mp2_information)

    duration_match      = re.search(r'Duration: (\d{2}:\d{2}:\d{2}\.\d{2})', info)
    duration            = duration_match.group(1) if duration_match else None

    resolution_match    = re.search(r'(\d{3,4}x\d{3,4})', info)
    resolution          = resolution_match.group(1) if resolution_match else None

    fps_match           = re.search(r'(\d+) fps', info)
    fps                 = fps_match.group(1) if fps_match else None

    bit_rate_match      = re.search(r'bitrate: (\d+) kb/s', info)
    bitrate             = bit_rate_match.group(1) if bit_rate_match else None

    sample_rate_match   = re.search(r'Stream #\d:\d: Audio: \w+, (\d+) Hz', info)
    sample_rate         = sample_rate_match.group(1) if sample_rate_match else None

    info_dict = {"Duration": duration,
                 "Resolution": resolution,
                 "BitRate": bitrate,
                 "SampleRate": sample_rate,
                 "FrameRate": fps}

    return info_dict
    

def ex1():

    bbb_file_path_mp4: str = "bbb.mp4"
    bbb_file_path_mp2: str = "bbb.mp2" 
    
    convert_to_mp2(bbb_file_path_mp4)
    
    information: subprocess.CompletedProcess[str] = get_info_from_video(bbb_file_path_mp2)
    video_info: dict = parse_video_information(information)
