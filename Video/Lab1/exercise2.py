# Ex 2 =======================================================================
'''
Use ffmpeg to resize images into lower quality and create a method  to
automate this process.
'''

import subprocess
from utils import *

def reduce_image_quality(input_file_path: str, 
                         output_file_path: str, 
                         quality: int) -> None:
    
    quality_vals = np.arange(2, 32, 1)
    if (quality not in quality_vals):
        quality = np.min(np.abs(quality), 31)

    cmd         = ["ffmpeg", "-i", input_file_path, "-q:v", str(quality), output_file_path]
    res         = subprocess.run(cmd, stdout = subprocess.PIPE, text = True)
    print(res, "\n")


def ex2() -> None:
    
    in_file_path        = "lena.png" 
    out_file_path_low   = "lena_low_quality.jpeg"
    out_file_path_high  = "lena_high_quality.jpeg"
    q1                  = 31
    q2                  = 2

    reduce_image_quality(input_file_path    = in_file_path, 
                         output_file_path   = out_file_path_low,
                         quality            = q1)
    
    reduce_image_quality(input_file_path    = in_file_path, 
                         output_file_path   = out_file_path_high,
                         quality            = q2)
        
    # Computing SNR
    original_image      = load_image(out_file_path_low).astype("uint8")
    compressed_image    = load_image(out_file_path_high).astype("uint8")
    snr                 = compute_snr(original_image, compressed_image)
    print(f"The signal to noise ratio of the chosen image is given by: {np.round(snr, 3)}", "\n")