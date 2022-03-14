from PIL import Image
import numpy as np
import os
from pathlib import Path
import pandas as pd

base_path = Path(__file__).parent.parent.parent
img_path = os.path.join(base_path, 'tests', 'assets', 'sample_image_kyoto.jpg')

# Load and return image information stored in Pandas df
def get_image_df(img_path):
    img = Image.open(img_path)
    imgar = np.asarray(img) # Convert Pillow img to np.array
    
    img_height, img_width = imgar.shape[0], imgar.shape[1]
    img_dim = img_height * img_width

    imgar_2d = imgar.reshape((img_dim, 3)) # Reshape 3d array to 2d for downstream pandas conversion

    df = pd.DataFrame(imgar_2d, columns=['pixel_r', 'pixel_g', 'pixel_b'])
    
    return df

# Returns the appropriate piecewise function to use given 
def get_hue_prime_pw(rgb_list, max_rgb):
    r, g, b = rgb_list[0], rgb_list[1], rgb_list[2]

    hue_prime_pw = { # Piecewise mathetmical definiion of hue' (aka length of RYGCP)
        #r: lambda c: ((g-b)/c) % 6, # Formula referenced on wikipedia, that may be incorrect
        r: lambda c: ((g-b)/c) + 6 if ((g-b)/c)<0 else ((g-b)/c), # 360/60 = 6 = deg shift for R° @ 0° to bring the segment above 0°
        g: lambda c: ((b-r)/c) + 2, # 120/60 = 2 = deg shift for G° @ 120° w/ ea hex side being 60°
        b: lambda c: ((r-g)/c) + 4, # 240/60 = 4 = deg shift for B° @ 240° w/ ea hex side being 60°
        0: lambda c: c
    } 

    pw = hue_prime_pw[max_rgb]
    return pw

# Add to RGB df: 
def df_rgb_to_hsl_list(df): 
    df['pixel_r_norm'] = df['pixel_r'].apply(lambda val: val/255)
    df['pixel_g_norm'] = df['pixel_g'].apply(lambda val: val/255)
    df['pixel_b_norm'] = df['pixel_b'].apply(lambda val: val/255)
    
    df['pixel_rgb_norm'] = df[['pixel_r_norm', 'pixel_g_norm', 'pixel_b_norm']].values.tolist()

    # Basic RGB properties used for calculation
    df['max_rgb'] = df['pixel_rgb_norm'].apply(max)
    df['min_rgb'] = df['pixel_rgb_norm'].apply(min)
    df['chroma'] = df['max_rgb'] - df['min_rgb']

    ## Hue Calculation
    df['h_prime_pw'] = df.apply(lambda x: get_hue_prime_pw(x['pixel_rgb_norm'], x['max_rgb']), axis=1)
    # Alternative speed runs:
    # - calc max rgb within get_hue_prime_pw
    # - input rgb individually rather than as a list
    # - dictionary lambda ref vs if match/case statements?
    # - directly obtaining hue_prime rather than having a col for pw


    df['h_prime_pw'] = df['FIX HERE'].apply(get_hue_prime_pw)
    # search if storing lambda functions in cols and using them later is possible
    df['h_prime'] = df['chroma'].apply(df['h_prime_pw'])
    df['pixel_h'] = df['h_prime'] * 60

    df['h_prime'] = df['chroma'].apply(hue_prime_pw[df['max_rgb']])
    df['pixel_h'] = df['h_prime'] * 60


def df_rgb_to_hsl_nolist(df):
    df['pixel_r_norm'] = df['pixel_r'].apply(lambda val: val/255)
    df['pixel_g_norm'] = df['pixel_g'].apply(lambda val: val/255)
    df['pixel_b_norm'] = df['pixel_b'].apply(lambda val: val/255)
    # currently takes 8.4s

    # Basic RGB properties used for calculation
    df['max_rgb'] = df.loc[:, 'pixel_r_norm':'pixel_b_norm'].apply(max, axis='columns')
    df['min_rgb'] = df.loc[:, 'pixel_r_norm':'pixel_b_norm'].apply(min, axis='columns')
    df['chroma'] = df['max_rgb'] - df['min_rgb']

    ## Hue Calculation
    for row in range(len(df)):
        r, g, b = df.loc[row, 'pixel_r_norm'], df.loc[row, 'pixel_g_norm'], df.loc[row, 'pixel_b_norm']
        max_rgb = df.loc[row, 'max_rgb']
        c = df.loc[row, 'chroma']
        
        if max_rgb == r:
            if ((g-b)/c)<0:
                h_prime = ((g-b)/c) + 6 
            else:
                h_prime = ((g-b)/c)
        elif max_rgb == g:
            h_prime = ((b-r)/c) + 2
        elif max_rgb == b:
            h_prime = ((r-g)/c) + 4
        elif max_rgb == 0:
            h_prime = 0
        df.loc[row, 'hue_prime'] = h_prime

    df['pixel_h'] = df['hue_prime'] * 60

    ## Luminance Calculation: Average of largest and smallest RGB components
    df['luminance'] = (df['max_rgb'] + df['min_rgb']) / 2 * 100 # unit: luminance%
    
    ## Saturation Calculation: Chroma scaled to fill [0,1]
    df['saturation'] = df['chroma'] / (1 - abs(2*(df['luminance']/100) - 1)) * 100 # unit: saturation%

    

## Array based conversion pixel-by-pixel (slow)
# Load and return image as 2d array
def get_image_array(img_path):
    img = Image.open(img_path)
    rgb_imgar = np.asarray(img) # Convert Pillow img to np.array

    return rgb_imgar

# Load and return reduced image as 2d array
def get_reduced_image_array(img_path, reduc_factor=10):
    img = Image.open(img_path)
    img = img.reduce(reduc_factor)
    rgb_imgar = np.asarray(img) # Convert Pillow img to np.array

    return rgb_imgar

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



## Array based conversion, but taking the full matrix rather than by per pixel
# rgb_imgar = get_image_array(img_path)

# Takes 3d array of rgb image, and returns hue, saturation, and luminance as 2d arrays
def get_hsl(rgb_imgar):
    rgb_imgar = rgb_imgar/255 # normalize rgb values
    
    r, g, b = rgb_imgar.T # Transposes 3d array, and separates into 2d color arrays
    
    min_rgb, max_rgb = np.min(rgb_imgar, 2).T, np.max(rgb_imgar, 2).T # Gets the min of each individual pixel, hence the 2 for order # (ex. 0,1,2)

    c = max_rgb - min_rgb # Chroma
    c_msk = c != 0 # Chroma mask/check for 0 vals (as hues will be kept @ 0 then)
   
    ## Hue Calculation
    h = np.zeros(r.shape)

    # Case when 'r' is max in pixel pt1 (negative radial shift)
    mask = (max_rgb == r) & c_msk & ((g-b)/c < 0) 
    h[mask] = (((g-b)/c) + 6)[mask] # 360/60 = 6 = deg shift for R° @ 0° to bring the segment above 0°
    # Case when 'r' is max in pixel pt2 (no radial shift)
    mask = (max_rgb == r) & c_msk & ((g-b)/c >= 0)
    h[mask] = ((g-b)/c)[mask]

    # Case when 'g' is max
    mask = (max_rgb == g) & c_msk
    h[mask] = (((b-r)/c) + 2)[mask] # 120/60 = 2 = deg shift for G° @ 120° w/ ea hex side being 60°

    # Case when 'b' is max
    mask = (max_rgb == b) & c_msk
    h[mask] = (((r-g)/c) + 4)[mask] # 240/60 = 4 = deg shift for B° @ 240° w/ ea hex side being 60°

    h *= 60 # unit: hue°

    ## Luminance Calculation: Average of largest and smallest RGB components
    l = (max_rgb + min_rgb) / 2 * 100 # unit: luminance%
    
    ## Saturation Calculation: Chroma scaled to fill [0,1]
    s = np.zeros(r.shape)
    s[c_msk] = (c / (1 - abs(2*(l/100) - 1)) * 100)[c_msk] # unit: saturation%

    return h, s, l

# Combines 2d h, s, l arrays into one 3d array to be ref'd as one image
def combine_hsl(h, s, l):
    hsl_imgar = np.zeros((h.shape[0], h.shape[1], 3))

    hsl_imgar[..., 0] = h # note: array[..., 0] == array[:,:,0]
    hsl_imgar[..., 1] = s
    hsl_imgar[..., 2] = l
    
    return hsl_imgar

# Format hsl matrix to be the same shape as the original rgb image matrix
def format_hsl(hsl_imgar):
    bx, by, bz = hsl_imgar.shape # the hsl_imgar has its x and y axis flipped from the original rgb_imgar
    new_imgar = hsl_imgar.copy().reshape(by, bx, bz)
    
    for row_indx in range(by): # by is referenced as axis 1 and 0 is switched in hsl_imgar
        row_new = hsl_imgar[:, row_indx] # In the current hsl_imgar, axis 1 = row_indx rather than the wanted col_indx 
        new_imgar[row_indx] = row_new # Hence, new_imgar's axis 0's relative row_indx is replaced with row_new
    
    return new_imgar

# Final exec function for converting given image file to hsl_matrix
def convert_img_to_hsl(img_path, reduced=True):
    if reduced:
        rgb_imgar = get_reduced_image_array(img_path)
    else:
        rgb_imgar = get_image_array(img_path)

    h, s, l = get_hsl(rgb_imgar)
    hsl_imgar = combine_hsl(h,s,l)
    hsl_imgar = format_hsl(hsl_imgar)

    return hsl_imgar

# Convert a 3d numpy array to a pandas dataframe
def array_to_df(imgar):
    names = ['ROW', 'COL', 'VAL']
    index = pd.MultiIndex.from_product([range(s) for s in imgar.shape], names=names)
    df = pd.DataFrame({'imgar': imgar.flatten()}, index=index)['imgar']

    df = df.unstack(level='VAL').swaplevel().sort_index()
    col_titles = ['HUE', 'SATURATION', 'LIGHTNESS']
    df.columns = col_titles

    return df

# Return a tuple of scorings for energy, loudness, and tempo
def df_scoring(df):
    energy = round(df['HUE'].mean()/36) # Normalize hue to a scale of 1-10
    loudness = round(df['SATURATION'].mean()/10)
    tempo = round(df['LIGHTNESS'].mean()/10)

    return (energy, loudness, tempo)
# imgar = np.random.randint(0,10, (5,4,3))
# 3/13, 4903x3262 image takes 21.2s to convert to df - compress images or just analyze arrays directly
# - compress image, do aggregate analysis with charles notes, create dictionary of val -> spotify api vals
# compression notes:
# - reducing the sample image by a factor of 10 decreased..
# -- hsl conversion from 3.9s to 0.2s
# -- df conversino from 21.2s to 0.1s

## Continue - Plot the hsl graphs to see clusters and also find summative data




## Testing in terminal
def testing_code():
    t = list(range(1,19))
    t = np.array(t).reshape(2,3,3)

    thsl = t.copy()
    thsl = np.array(thsl, dtype=float) # Don't know why, but this is needed to keep floats
    for i, matrix in enumerate(thsl):
        for j, arr in enumerate(matrix):
            print(f'At position ({i}, {j}):')
            print(f'starting pixel: {arr}')
            hsl = rgb_to_hsl_pixel(arr)
            tf = hsl[0]
            ty = type(tf)
            print(f'pixel to hsl: {hsl} as type {ty} (first val: {tf})')

            thsl[i,j] = hsl
            sample = thsl[i,j]
            tya = type(thsl[i,j][0])
            print(f'pixel after change: {sample} as type {tya}')
            print('\n')
