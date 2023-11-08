import subprocess
import utils

def modify_chroma_subsampling(video_file_path: str, subsampling_scheme: str) -> None:

    video_out_name = utils.parse_extension(video_file_path)[0] + "_" + subsampling_scheme + ".mp4"
    cmd = ["ffmpeg", 
           "-i", 
           video_file_path,
           "-pix_fmt",
           subsampling_scheme,
           "-c:a",
           "copy",
           video_out_name]  # copiamos el audio tal cual
    
    try:
        subprocess.run(cmd)
    except: 
        print("Please check your video path and/or subsampling scheme.")


def ex3():
    
    video_fp    = "bbb.mp4"
    chroma      = "yuv420p"  
    modify_chroma_subsampling(video_file_path       = video_fp,
                              subsampling_scheme    = chroma)