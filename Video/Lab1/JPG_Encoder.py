# Ex 6 =======================================================================
'''
Create a class which can convert, can decode
(or both) an input using the DCT. Not necessary a
JPG encoder or decoder. A class only about DCT is
OK too
'''

import numpy as np
from Video.Lab1.RGB_Translator import Translator
from PIL import Image
from scipy.fftpack import dct
from Video.Lab2.utils import *

class JPEGEncoder:

    def __init__(self, quality: float) -> None:

        quality = np.clip(1, 100, quality)

        if (quality < 50):
            quality = 5000 / quality
        else:
            quality = 200 - quality * 2 
        
        self.quantisation_table = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                            [12, 12, 14, 19, 26, 58, 60, 55],
                                            [14, 13, 16, 24, 40, 57, 69, 56],
                                            [14, 17, 22, 29, 51, 87, 80, 62],
                                            [18, 22, 37, 56, 68, 109, 103, 77],
                                            [24, 35, 55, 64, 81, 104, 113, 92],
                                            [49, 64, 78, 87, 103, 121, 120, 101],
                                            [72, 92, 95, 98, 112, 100, 103, 99]])
        
        self.scaled_quant_table = np.floor((self.quantisation_table * quality + 50) / 100)
        self.scaled_quant_table[self.scaled_quant_table < 1] = 1

    def set_image(self, image: np.ndarray) -> None:
        self.image_to_encode    = image
        self.translator         = Translator() 

    def get_image(self) -> np.ndarray:
        return self.image_to_encode
    
    def preprocess(self) -> None:
        self.image_to_encode = self.translator.transform_image_rgb_to_yuv(self.image_to_encode)
        
    def truncate_to_multiples_of_8(self):
        height, width   = self.image_to_encode.shape[:2]
        new_height      = (height // 8) * 8
        new_width       = (width // 8) * 8
        
        self.image_to_encode = self.image_to_encode[:new_height, :new_width, ...]

    def apply_zig_zag(self, block: np.ndarray) -> np.ndarray:
        
        h = 0
        v = 0

        vmin = 0
        hmin = 0

        vmax = block.shape[0]
        hmax = block.shape[1]
        
        i = 0

        output = np.zeros(( vmax * hmax))
        
        #----------------------------------

        while ((v < vmax) and (h < hmax)):
            if ((h + v) % 2) == 0:
                if (v == vmin):
                    output[i] = block[v, h]       

                    if (h == hmax):
                        v = v + 1
                    else:
                        h = h + 1                        

                    i = i + 1

                # if we got to the last column
                elif ((h == hmax -1 ) and (v < vmax)):
                    output[i] = block[v, h] 
                    v = v + 1
                    i = i + 1

                # all other cases
                elif ((v > vmin) and (h < hmax -1 )):
                    output[i] = block[v, h]
                    v = v - 1
                    h = h + 1
                    i = i + 1

            else:
                if ((v == vmax -1) and (h <= hmax -1)):
                    output[i] = block[v, h]
                    h = h + 1
                    i = i + 1
                    
                elif (h == hmin):
                    output[i] = block[v, h] 
                    
                    if (v == vmax -1):
                        h = h + 1
                    else:
                        v = v + 1
                    
                    i = i + 1

                elif ((v < vmax -1) and (h > hmin)):
                    output[i] = block[v, h]
                    v = v + 1
                    h = h - 1
                    i = i + 1

            if ((v == vmax-1) and (h == hmax-1)):
                output[i] = block[v, h]
                break

        return output


    def apply_dct_to_block(self, block: np.ndarray) -> np.ndarray:
        assert(block.shape == (8, 8))
        dct_block       = dct(dct(block.T, norm = "ortho").T, norm = "ortho")
        quantised_block = np.round(dct_block / self.scaled_quant_table) 
        return quantised_block
    
    def apply_dct_to_image(self) -> None:
        block_size = 8
        self.encoded_image  = np.array([])
        for ch in range(3):
            for r_idx in range(0, self.image_to_encode.shape[0], 8):
                for c_idx in range(0, self.image_to_encode.shape[1], 8):
                    current_block       = self.image_to_encode[r_idx:r_idx + block_size, c_idx:c_idx + block_size, ch]
                    quantised_block     = self.apply_dct_to_block(current_block)
                    np.append(self.encoded_image, self.apply_zig_zag(quantised_block))
        
        self.encoded_image = np.array(self.encoded_image)
    

    def encode_input(self) -> bytes:
        
        self.preprocess()                   # Step 1: Convert image to YUV colour space
        self.truncate_to_multiples_of_8()   # Step 2: Truncate dimensions of image to multiples of 8 (dct prep)
        self.apply_dct_to_image()           # Step 3: Apply DCT + Quantise 
        
        data_in_bytes = bytes(self.encoded_image)
        return self.apply_run_length_encoding(data_in_bytes) # Step 4: Apply run length encoding
        
    def apply_run_length_encoding(self, data_in_bytes: bytes) -> bytes:
        run_length_coding = [] 
        count = 1
    
        for idx in range(1, len(data_in_bytes)):
            
            if data_in_bytes[idx] == data_in_bytes[idx - 1] and data_in_bytes[idx] == 0:
                count += 1
            else:
                if (data_in_bytes[idx - 1] == 0):
                    print("Zero detected")
                    run_length_coding.extend([data_in_bytes[idx - 1], count])
                else:
                    run_length_coding.extend([data_in_bytes[idx - 1]])
                count = 1

            if (data_in_bytes[-1] == 0):
                run_length_coding.extend([data_in_bytes[-1], count])
            else:
                run_length_coding.extend([data_in_bytes[-1]])
                
        return bytes(run_length_coding)
        

def ex6():
    enc     = JPEGEncoder(quality = 40) 
    lena    = load_image("lena.png")
    
    enc.set_image(lena)
    enc.encode_input()

    return 