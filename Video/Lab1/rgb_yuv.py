import numpy as np
import typing

# Ex 1 =======================================================================
'''
1) Start a script called rgb_yuv.py and create a
translator from 3 values in RGB into the 3 YUV
values, plus the opposite operation. 
'''

class Translator:

    def __init__(self) -> None:
        self.rgb_to_yuv_coeffs = np.array([ [0.257, 0.504, 0.098, 16],
                                            [-0.148, -0.291, 0.439, 128],
                                            [0.439, -0.368, -0.071, 128]])
        

        self.yuv_to_rgb_coeffs = np.array([ [1.164, 0, 1.596],
                                            [1.164, -0.392, -0.813],
                                            [1.164, 2.017, 0]])

    def rgb_to_yuv(self, r: float, g: float, b: float) -> np.ndarray:
        c = self.rgb_to_yuv_coeffs
        y = r * c[0, 0] + g * c[0, 1] + b * c[0, 2] + 16
        u = r * c[1, 0] + g * c[1, 1] + b * c[1, 2] + 128
        v = r * c[2, 0] + g * c[2, 1] + b * c[2, 2] + 128

        return np.array([y, u, v])
    
    def yuv_to_rgb(self, y: float, u: float, v: float) -> np.ndarray:
        c = self.yuv_to_rgb_coeffs
        r = (y - 16) * c[0, 0] + (u - 128) * c[0, 1] + (v - 128) * c[0, 2]
        g = (y - 16) * c[1, 0] + (u - 128) * c[1, 1] + (v - 128) * c[1, 2]
        b = (y - 16) * c[2, 0] + (u - 128) * c[2, 1] + (v - 128) * c[2, 2]
        return np.array([r, g, b])
    

def ex1():
    t = Translator()
    rgb_vals = np.array([12, 44, 188])
    print(f"Original RBG Values: {rgb_vals} \n")

    # Conversion (RGB to YUV)
    yuv_vals = t.rgb_to_yuv(r = rgb_vals[0],
                            g = rgb_vals[1],
                            b = rgb_vals[2])
    
    # Conversion (YUV to RBG)
    print(f"After YUV Conversion: {yuv_vals}")
    new_rgb_vals = t.yuv_to_rgb(y = yuv_vals[0],
                                u = yuv_vals[1],
                                v = yuv_vals[2])
    
    print(f"Converting YUV values back to RGB: {new_rgb_vals}")
    print(f"After Concatenating to int: {new_rgb_vals.astype(int)}")
    print(f"Conversion Loss: {np.abs(new_rgb_vals.astype(int) - new_rgb_vals)}")


# Ex 2 =======================================================================
'''
2) Use ffmpeg to resize images into lower quality and create a method  to
automate this process.
'''

import subprocess
from PIL import Image

def load_image(file_path: str) -> np.ndarray:
    image = Image.open(file_path)
    return np.array(image)

def compute_snr(original_image: np.ndarray, compressed_image: np.ndarray) -> float:
    if original_image.shape != compressed_image.shape:
        print(f"Original shape: {original_image.shape}", f"Compressed Image: {compressed_image.shape}")
        raise ValueError("Both images must have the same shape.")

    original_mean_square    = np.mean(original_image ** 2)
    noise                   = original_image - compressed_image
    noise_mean_square       = np.mean(noise ** 2)

    snr = 10 * np.log10(original_mean_square / noise_mean_square)
    return snr


def parse_extension(file_path_with_extension: str) -> tuple[str, str]:
    components = file_path_with_extension.split(".")
    assert(len(components) == 2)

    file_path = components[0]
    extension = components[1]
    return (file_path, extension)

def parse_file_name(file_path: str) -> str:
    subdirectories = file_path.split("/")
    return subdirectories[-1]

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
    # Customise paths
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

# Ex 3 =======================================================================
'''
3) Create a method called serpentine which should
be able to read the bytes of a JPEG file in the
serpentine way we saw.
'''

def serpentine(image: np.ndarray):
    
    r_start_idx = 0
    c_start_idx = 0
    r_end_idx   = image.shape[0]
    c_end_idx   = image.shape[1]

def ex3():
    return


def main():
    #ex1()
    #ex2()
    ex3()

if __name__ == "__main__":
    main()
