# Ex 3 =======================================================================
'''
Create a method called serpentine which should
be able to read the bytes of a JPEG file in the
serpentine way we saw.
'''
import numpy as np

# lifted from https://github.com/getsanjeev/compression-DCT/blob/ba9d65af366f2baa314ab2c1bac94f5eb9211be3/zigzag.py
def zigzag(input: np.ndarray) -> np.ndarray:
    
    h = 0
    v = 0

    vmin = 0
    hmin = 0

    vmax = input.shape[0]
    hmax = input.shape[1]
    
    i = 0

    output = np.zeros(( vmax * hmax))
    
    #----------------------------------

    while ((v < vmax) and (h < hmax)):
        if ((h + v) % 2) == 0:
            if (v == vmin):
                output[i] = input[v, h]       

                if (h == hmax):
                    v = v + 1
                else:
                    h = h + 1                        

                i = i + 1

            # if we got to the last column
            elif ((h == hmax -1 ) and (v < vmax)):
                output[i] = input[v, h] 
                v = v + 1
                i = i + 1

            # all other cases
            elif ((v > vmin) and (h < hmax -1 )):
                output[i] = input[v, h]
                v = v - 1
                h = h + 1
                i = i + 1

        else:
            if ((v == vmax -1) and (h <= hmax -1)):
                output[i] = input[v, h]
                h = h + 1
                i = i + 1
                
            elif (h == hmin):
                output[i] = input[v, h] 
                
                if (v == vmax -1):
                    h = h + 1
                else:
                    v = v + 1
                
                i = i + 1

            elif ((v < vmax -1) and (h > hmin)):
                output[i] = input[v, h]
                v = v + 1
                h = h - 1
                i = i + 1

        if ((v == vmax-1) and (h == hmax-1)):
            output[i] = input[v, h]
            break

    return output

def ex3():

    test_matrix = np.array([[1, 2, 3, 4, 5, 6, 7, 8],
                            [9, 10, 11, 12, 13, 14, 15, 16],
                            [17, 18, 19, 20, 21, 22, 23, 24],
                            [25, 26, 27, 28, 29, 30, 31, 32],
                            [33, 34, 35, 36, 37, 38, 39, 40],
                            [41, 42, 43, 44, 45, 46, 47, 48],
                            [49, 50, 51, 52, 53, 54, 55, 56],
                            [57, 58, 59, 60, 61, 62, 63, 64]])
    
    res = zigzag(test_matrix)
    print(res)