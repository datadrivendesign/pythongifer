#!/usr/bin/env python
from images2gif import writeGif
from PIL import Image
import os
import glob
import re

## Provides sorting based on the frame number
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

## Import the file names
file_names = sorted(glob.glob('res/img/*.png'), key=numericalSort)

# Read inputEvents.txt
inputEvents = open('res/inputEvents.txt', 'r')
events = inputEvents.readlines();
frameBreaks = [0]

# Regex pattern match
for e in events:
    frame = int(re.search('imgCount:([0-9]+)', e).group(1))
    if not frameBreaks:
        frameBreaks.append(frame)
    elif not frame in frameBreaks:
        frameBreaks.append(frame)

gifCount = 1
for x in range(len(frameBreaks)-1):
    images = []

    for y in range(frameBreaks[x], frameBreaks[x+1]):
        images.append(Image.open(file_names[y]));

    size = (600,350)
    for im in images:
        im.thumbnail(size, Image.ANTIALIAS)
    filename = "sequence" + str(gifCount) + ".gif"
    writeGif("gifs/" + filename, images, duration=0.1)
    for y in images:
        y.close()
    gifCount += 1

inputEvents.close()
