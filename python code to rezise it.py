# Resize all Images in a Directory

import PIL
from PIL import Image, ImageOps
import os

directory = 'C:\\Users\\Thiago\\Desktop'#SPECIFY THE DIRECTORY!
for file in os.listdir(directory):
    if file.endswith(('jpeg', 'png', 'jpg')):
        filepath = os.path.join(directory, file)
        outfile = os.path.join(directory, 'resized_'+file)
        with Image.open(directory+'/'+file) as im:
            #im.resize((1024, 600), resample=None, box=(50,50,200,200), reducing_gap=None) **DIDN'T WORK**
            new_size = im.resize((1024, 600), resample=None, box=None, reducing_gap=None)
            #im = ImageOps.pad(im, (1024, 600), color='grey')**DIDN'T WORK**
            #im = ImageOps.fit(im, (1024, 600))**DIDN'T WORK**
            new_size.save(outfile)
            #im.save(outfile)
print('finished! check the folder to see if it worked!')
