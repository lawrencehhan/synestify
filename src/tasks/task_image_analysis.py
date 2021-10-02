from PIL import Image
import numpy as np
import os
from pathlib import Path
import pandas as pd

base_path = Path(__file__).parent.parent
img_path = os.path.join(base_path, 'tests', 'assets', 'test_image_01_kyoto.jpg')

# Load and return image as 2d array
def get_2d_image(img_path):
    img = Image.open(img_path)
    imgar = np.asarray(img) # Convert Pillow img to np.array
    
    img_height, img_width = imgar.shape[0], imgar.shape[1]
    img_dim = img_height * img_width

    imgar_2d = imgar.reshape((img_dim, 3)) # Reshape 3d array to 2d for downstream pandas conversion

    df = pd.DataFrame()
    
    return imgar_2d

# Returns normalized rgb np.array
def normalize_rgb(rgb):
    rgb_n = [val/255 for val in rgb]
    return rgb_n  

# Takes an rgb array [r,g,b] and returns its hsl (hue, sat%, light%) equivalent 
def rgb_to_hsl_pixel(rgb):
    rgb_n = normalize_rgb(rgb)
    r, g, b = rgb_n[0], rgb_n[1], rgb_n[2] # normalized rgb values split

    max_rgb = max(r,g,b)
    min_rgb = min(r,g,b)
    chroma = max_rgb - min_rgb # 'Roughly the dist from the point of origin' (radial dimension) Note: normalized

    ## Hue Calculation
    hue_prime_pw = { # Piecewise mathetmical definiion of hue' (aka length of RYGCP)
        #r: lambda c: ((g-b)/c) % 6,
        r: lambda c: ((g-b)/c) + 6 if ((g-b)/c)<0 else ((g-b)/c), # 360/60 = 6 = deg shift for R° @ 0° to bring the segment above 0°
        g: lambda c: ((b-r)/c) + 2, # 120/60 = 2 = deg shift for G° @ 120° w/ ea hex side being 60°
        b: lambda c: ((r-g)/c) + 4, # 240/60 = 4 = deg shift for B° @ 240° w/ ea hex side being 60°
        0: lambda c: c
    }

    hue_prime = hue_prime_pw[max_rgb](chroma) # Applying appropriate hue piecewise func given max_rgb
    h = hue_prime * 60 # unit: hue°

    ## Luminance Calculation: Average of largest and smallest RGB components
    l = (max_rgb + min_rgb) / 2 * 100 # unit: luminance%
    
    ## Saturation Calculation: Chroma scaled to fill [0,1]
    if chroma == 0: # max and min are the same => no saturation
        s = 0
    else:
        s = chroma / (1 - abs(2*(l/100) - 1)) * 100 # unit: saturation%

    hsl = np.asarray([h, s, l])
    return hsl


# Converts every pixel in an array type image from RGB to HSL
def rgb_to_hsl_imgar(imgar):
    img_height = imgar.shape[0]
    img_width = imgar.shape[1]
    hsl_imgar = np.zeros([img_height, img_width, 3])

    for h in range(img_height):
        for w in range(img_width):
            rgb_pixel = imgar[h, w]
            hsl_pixel = rgb_to_hsl_pixel(rgb_pixel)
            
            hsl_imgar[h, w] = hsl_pixel

            print(f'Pixel @ {h}x{w}: {hsl_pixel}')
    
    return hsl_imgar