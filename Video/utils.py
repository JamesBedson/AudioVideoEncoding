from PIL import Image
import numpy as np
import subprocess

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

def parse_sub_directories(file_path: str) -> str:
    return file_path.replace(parse_file_name(file_path), "") 

def cut_video_duration(in_fp: str, out_fp: str, start_time: str, end_time: str) -> None:
    
    cmd         = ["ffmpeg", "-i", in_fp, "-ss", start_time, "-to", end_time, out_fp]
    subprocess.run(cmd)