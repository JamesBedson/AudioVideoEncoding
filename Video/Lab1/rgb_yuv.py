import numpy as np
import typing

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


def main():
    ex1()
    
if __name__ == "__main__":
    main()
