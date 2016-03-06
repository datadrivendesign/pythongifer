#!/usr/bin/env python
from images2gif import writeGif
from PIL import Image, ImageDraw
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
events = inputEvents.readlines()
inputEvents.close()
frameBreaks = [0]
eventCoords = []

# Regex pattern match
for e in events:
    frame = int(re.search('imgCount:([0-9]+)', e).group(1))
    x = re.search('x:(\d+\.\d+)', e)
    y = re.search('y:(\d+\.\d+)', e)
    if not frame in frameBreaks:
        frameBreaks.append(frame)
    if x is not None and y is not None:
        eventCoords.append( ( float(x.group(1)) , float(y.group(1)) ) )


# Remove all old files
files = glob.glob('gifs/*')
for f in files:
    os.remove(f)

# Modify to change properties of GIFs
frameSkip = 3
durationVal = 0.2
length = 600
width = 350
#circle = (0, 0, 40, 40)

gifCount = 0

for x in range(len(frameBreaks)-1):

    if (frameBreaks[x+1] - frameBreaks[x]) > 10:
        images = []
        for y in range(frameBreaks[x], frameBreaks[x+1], frameSkip):
            images.append(Image.open(file_names[y]))

        size = (length,width)
        for im in images:
            im.thumbnail(size, Image.ANTIALIAS)

        for i in (0,3):
            draw = ImageDraw.Draw(images[i])
            circle = (eventCoords[i][0], eventCoords[i][1], 40, 40)
            draw.ellipse(circle, fill='blue')
            del draw

        filename = "sequence" + str(gifCount) + ".gif"
        writeGif("gifs/" + filename, images, duration=durationVal)
        for i in images:
            i.close()
        gifCount += 1
