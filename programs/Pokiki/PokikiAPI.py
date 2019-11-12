import cv2
from programs.Pokiki.Helper import HelperOBJ, getAverageColor, splitRow
import numpy as np
from pathlib import Path
from PIL import Image
from multiprocessing import Pool, cpu_count
import time
from functools import partial
import os

helperOBJ = HelperOBJ()

def convertFromFiles(file_dirs, options_list):
    for file_dir, options in zip(file_dirs, options_list):
        convertFromFile(file_dir, options)

def convertFromFile(file, options, saveTo=None):
    convertFromImage(Image.open(file), options, saveTo=saveTo)

def convertFromImages(img_list, options_list):
    for img, options in zip(img_list, options_list):
        convertFromImage(img, options)

def convertFromImage(img, options, saveTo=None):
    quality = int(options["Q"])
    splitByHorizontal = int(options["X"])
    splitByVertical = int(options["Y"])

    # Convert transparent pixels to white
    if img.format == "PNG":
        rgba_img = img.convert("RGBA")
        img = Image.new("RGB", img.size, "WHITE")
        img.paste(rgba_img, (0, 0), rgba_img)

    startTime = time.time()
    time.clock()    

    picDeconstructTime = time.time()
    pictureW, pictureH = img.size

    rowH = pictureH / splitByVertical
    rowW = pictureW / splitByHorizontal
    rows = []
    for section_index in range(0, splitByVertical):
        section = (0, rowH * section_index, pictureW, rowH * (section_index + 1))
        row = img.crop(section)
        rows.append(row)
    
    elapsed = time.time() - picDeconstructTime
    print('Image deconstruction:', elapsed)

    threadingTime = time.time()
    with Pool(processes=cpu_count()) as pool:
        func = partial(helperOBJ.buildRows, splitByHorizontal, splitByVertical, quality)
        result_rows = pool.map(func, rows)    

    elapsed = time.time() - threadingTime
    print('Threading:', elapsed)

    assemblyTime = time.time()
    resultIMG = None
    firstRowH, firstRowW, _ = result_rows[0].shape
    for row in result_rows:
        if resultIMG is None:
            resultIMG = row
        else:
            row = cv2.resize(row, (firstRowW,firstRowH), interpolation=cv2.INTER_CUBIC)
            resultIMG = np.vstack((resultIMG, row))

    elapsed = time.time() - assemblyTime
    print('Image construction:', elapsed)

    elapsed = time.time() - startTime
    print('Total elapsed time:', elapsed)

    if not os.path.isdir(os.path.dirname(saveTo)):
        os.makedirs(os.path.dirname(saveTo))
        
    filename, file_extension = os.path.splitext(saveTo)
    
    if file_extension == "png" or file_extension == "PNG":
        cv2.imwrite(saveTo, resultIMG, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    else:
        cv2.imwrite(saveTo, resultIMG, [cv2.IMWRITE_JPEG_QUALITY, 35])

    