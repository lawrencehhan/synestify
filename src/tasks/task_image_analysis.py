from PIL import Image
import numpy as np
import os
from pathlib import Path
import pandas as pd

base_path = Path(__file__).parent.parent.parent
img_path = os.path.join(base_path, 'tests', 'assets', 'sample_image_darkwindow.jpg')
img_path = os.path.join(base_path, 'tests', 'assets', 'sample_image_kyoto.jpg')

## Array based conversion method for image-to-hsl_array

# Load and return image as 2d array
def get_image_array(img_path, reduc_factor=1):
    img = Image.open(img_path).reduce(reduc_factor)
    rgb_imgar = np.asarray(img) # Convert Pillow img to np.array

    return rgb_imgar

# Load and return image as 2d array at a reduced size
def get_reduced_image_array(img_path, reduc_factor):
    img = Image.open(img_path).reduce(reduc_factor)
    rgb_imgar = np.asarray(img) # Convert Pillow img to np.array

    return rgb_imgar

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

# Converting given RGB np.array to an HSL array matrix
def convert_rgb_to_hsl(rgb_imgar):
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
    energy = round(df['HUE'].mean()/360, 2) # Normalize hue to a scale of 0-1 from 0-360
    loudness = round(df['SATURATION'].mean()/100, 2)
    tempo = ((170-70)*((df['LIGHTNESS'].mean()-0)/100))+70 # Tempo normalized to 70-170 range
    tempo = round(tempo, 2)
    return (energy, loudness, tempo)

# Wrapped up executable function to collect scores from raw image file
def get_image_score(img_path, reduc_factor):
    rgb_imgar = get_image_array(img_path, reduc_factor)
    hsl_imgar = convert_rgb_to_hsl(rgb_imgar)
    df = array_to_df(hsl_imgar)
    scores = df_scoring(df)

    return scores
