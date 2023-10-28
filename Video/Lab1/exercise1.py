# Ex 1 =======================================================================
'''
Start a script called rgb_yuv.py and create a
translator from 3 values in RGB into the 3 YUV
values, plus the opposite operation. 
'''
import numpy as np
from PIL import Image
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
    
    def transform_image_rgb_to_yuv(self, image: np.ndarray) -> np.ndarray:

        c       = self.rgb_to_yuv_coeffs 
        r_ch    = image[:,:,0]
        g_ch    = image[:,:,1]
        b_ch    = image[:,:,2]

        y_ch    = r_ch * c[0, 0] + g_ch * c[0, 1] + b_ch * c[0, 2] + 16
        u_ch    = r_ch * c[1, 0] + g_ch * c[1, 1] + b_ch * c[1, 2] + 128
        v_ch    = r_ch * c[2, 0] + g_ch * c[2, 1] + b_ch * c[2, 2] + 128

        yuv_img = np.stack([y_ch, u_ch, v_ch], axis=-1)
        return np.clip(yuv_img, 0, 255).astype(np.uint8)
    

    def transform_image_yuv_to_rgb(self, image: np.ndarray) -> np.ndarray:
        c       = self.yuv_to_rgb_coeffs
        y_ch    = image[:,:,0]
        u_ch    = image[:,:,1]
        v_ch    = image[:,:,2]

        r_ch    = (y_ch - 16) * c[0, 0] + (u_ch - 128) * c[0, 1] + (v_ch - 128) * c[0, 2]
        g_ch    = (y_ch - 16) * c[1, 0] + (u_ch - 128) * c[1, 1] + (v_ch - 128) * c[1, 2]
        b_ch    = (y_ch - 16) * c[2, 0] + (u_ch - 128) * c[2, 1] + (v_ch - 128) * c[2, 2]

        rgb_img = np.stack([r_ch, g_ch, b_ch], axis=-1)
        return np.clip(rgb_img, 0, 255).astype(np.uint8)



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