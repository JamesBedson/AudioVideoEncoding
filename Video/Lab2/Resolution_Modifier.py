import subprocess
import utils as utl

def modify_resolution(video_file_path: str, resolution_wh: tuple[int, int]) -> None:
    
    file_path_name = utl.parse_extension(video_file_path)[0]
    cmd = ["ffmpeg", 
           "-i", 
           video_file_path, 
           "-vf", 
           f"scale={resolution_wh[0]}:{resolution_wh[1]}", 
           file_path_name + f"_{resolution_wh[0]}_{resolution_wh[1]}.mp4"]
    
    try: 
        subprocess.run(cmd)

    except subprocess.CalledProcessError: 
        print("Conversion failed. Please check your target resolution and/or file path.")

def ex2():
    fp = "bbb.mp4"
    modify_resolution(video_file_path = fp, 
                      resolution_wh = (320, 240))