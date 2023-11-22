import subprocess

def extract_yuv_hist(video_fp) -> None:
    
    cmd = [
        "ffmpeg",
        "-i", video_fp,
        "-vf", f"split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay",
        "output_with_histogram.mp4"
    ]
    subprocess.run(cmd, capture_output = False, text = True)
    
