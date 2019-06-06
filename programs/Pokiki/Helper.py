import numpy as np
import cv2
from scipy.stats import itemfreq
import json
import math
from PIL import Image
from pathlib import Path

class HelperOBJ:

    def __init__(self):
        self.rootFolder = Path('./programs/Pokiki')

        self.tilesFolder = self.rootFolder / "tiles/"

        self.dataFile = self.rootFolder / 'out/data.json'

        self.data = json.loads(open(str(self.dataFile)).read())

    def findNearestNeighbor(self, color, dominant=False):
        r, g, b = color[0], color[1], color[2]
        closest = None

        for index, imgData in enumerate(self.data):
            avg_color = imgData['average_color']
            r_candit, g_candit, b_candit = avg_color[0], avg_color[1], avg_color[2]
            closeness = math.sqrt((r-r_candit)**2 + (g-g_candit)**2 + (b-b_candit)**2)

            if closest is None or closest[0] >= closeness:
                closest = [closeness, imgData["name"]]

        return closest[1]

    def buildRows(self, splitByHorizontal, splitByVertical, quality, picture_section):
        columns = None
        columnCount = 0
        firstColH = None
        firstColW = None
        for count, img in enumerate(splitRow(picture_section, splitByHorizontal, splitByVertical)):
            open_cv_IMG = np.array(img, dtype='uint8')
            # open_cv_IMG = cv2.cvtColor(open_cv_IMG, cv2.COLOR_RGBA2BGRA)

            tile_color = getAverageColor(open_cv_IMG) 
            tile_pic_path = self.tilesFolder / self.findNearestNeighbor(tile_color)
            
            windowW, windowH = img.size
            window_aspect_ratio = float(windowW) / float(windowH)
            # print("Win ar:", window_aspect_ratio)

            tile_pic = cv2.imread( str(tile_pic_path), cv2.IMREAD_COLOR)
            tile_pic = cv2.resize(tile_pic, (151, 172))
            tile_pic = cv2.resize(tile_pic, (0, 0), fx=0.2,fy=0.2, interpolation=cv2.INTER_CUBIC)
            if quality <= 0: quality = 1
            
            tile_pic = cv2.resize(tile_pic, (0,0), fx=window_aspect_ratio*quality, fy=quality, interpolation=cv2.INTER_CUBIC)

            if firstColH is None and firstColW is None:
                firstColH, firstColW, _ = tile_pic.shape

            if columns is None:
                columns = tile_pic
                columnCount += 1
            elif columnCount < (splitByHorizontal - 1):
                tile_pic = cv2.resize(tile_pic, (firstColW,firstColH), interpolation=cv2.INTER_CUBIC)
                columns = np.hstack((columns, tile_pic))
                columnCount += 1
            else:
                return columns

def getAverageColor(img):
    return [img[:, :, i].mean() for i in range(img.shape[-1])]

def loadFileJSON(file):
    dataFileStr = open(file).read()

    return json.loads(dataFileStr)

def splitRow(input_picture, splitByHorizontal, splitByVertical):
    width, boxH = input_picture.size
    boxW = width/splitByHorizontal
    width_steps = np.arange(0, width, boxW)
    for j in width_steps:
        box = (j, 0, j + boxW, boxH)
        yield input_picture.crop(box)

def splitImg(input_picture, splitByHorizontal, splitByVertical):
    width, height = input_picture.size
    boxH, boxW = height/splitByVertical, width/splitByHorizontal
    height_steps = np.arange(0, height, boxH)
    width_steps = np.arange(0, width, boxW)
    # height_steps = [boxH * x for x in range(0, splitByVertical)]
    # width_steps = [boxW * x for x in range(0, splitByHorizontal)]
    for i in height_steps: # range(0, height, int(boxH)):
        for j in width_steps: # range(0, width, int(boxW)):
            box = (j, i, j + boxW, i + boxH)
            yield input_picture.crop(box)
