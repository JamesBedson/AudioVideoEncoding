import subprocess
import Video.utils as utils
from MP2_Converter import get_info_from_video, parse_video_information

def print_video_info(video_file_path: str):
    info = get_info_from_video(video_file_path)
    info_dict = parse_video_information(info)
    
    print()
    print(f"Video Information for: {video_file_path}")
    print("Duration:", info_dict["Duration"])
    print("Resolution:", info_dict["Resolution"])
    print("Bitrate:", info_dict["BitRate"])
    print("Sample Rate:", str(info_dict["SampleRate"]) + "[Hz]")
    print("Frame Rate:", info_dict["FrameRate"])


def ex4():

    video_fp = "bbb.mp4"
    print_video_info(video_fp)

    return
