# Ex 4 =======================================================================
from utils import *

'''
Use FFMPEG to transform the previous image
into b/w. Do the hardest compression you can.
Add everything into a new method and comment
the results
'''

def b_w_compression(in_file_path: str) -> None:
    
    in_name     = parse_file_name(in_file_path)
    out_name    = parse_sub_directories(in_file_path) + f"{in_name}" + "_bw_compressed.jpg"

    cmd = ["ffmpeg", "-i", in_file_path, "-vf", "hue=s=0'", "-q:v", str(31), out_name] 
    #hue and saturation = 0 --> grayscale
    #hardest compression setting of a jpeg --> q = 31
    
    res = subprocess.run(cmd, stdout = subprocess.PIPE, text = True)
    print(res, "\n")

def ex4():

    input_file_path = "lena.png"
    b_w_compression(input_file_path)