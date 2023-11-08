import Lab1.Image_Q_Reducer as l1ex2
import Lab1.Zigzag_Algorithm as l1ex3

import imageio
import numpy as np

def read_video_as_numpy(video_path: str) -> np.ndarray:
    video = imageio.get_reader(video_path)
    frames = [frame for frame in video]         #type:ignore
    return np.array(frames)


def ex5():
    
    bbb = read_video_as_numpy("bbb.mp4")
    snr = l1ex2.compute_snr(bbb[0], bbb[1])
    print(snr)

    zigzag = l1ex3.zigzag(bbb[0])
    print(zigzag)
