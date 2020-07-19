#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 07/15/2020
# FILENAME: indy_augmentation.py
#
###############################################################################
# INFO:
# - Script to augment a set of prelabeled images with bounding boxes.
# - Uses python3 and imgaug library.
#
#
###############################################################################


import imageio
from imgaug import augmenters as iaa
from matplotlib import pyplot as plt
import numpy as np
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import xml.etree.ElementTree as ET

def getBoundingBox(filename):
    # parses XML file for bounding box coordinates for single object and box
    root = ET.parse(filename).getroot()
    coords = []
    for i in range(4):
        val = int(root[6][4][i].text)
        coords.append(val)
    return coords

def getAllFiles(PATH,filename):
    # makes list of all files in chosen directory
    fileNames = []
    for i in range(len(folderSize//2)):
        numLabel = "{:0>3d}".format(i)
        currFile = filename + numLabel
        fileNames.append(currFile)
    return fileNames

def generateNewImage(newFilename):
    # generates new image file and saves in chosen directory
    return 42

def generateNewXML(newFilename):
    # generates new xml file and saves in chosen directory
    return 42


filename = 'racecar004'
xml = '.xml'
jpg = '.jpg'
# use imageio library to read the image (alternatively you can use OpenCV cv2.imread() function)
image = imageio.imread('racecar004.jpg')
xmlbox = getBoundingBox(filename + xml)
box_x1 = xmlbox[0]
box_y1 = xmlbox[1]
box_x2 = xmlbox[2]
box_y2 = xmlbox[3]




# Initialize the bounding box for the original image
# using helpers from imgaug package
bbs = BoundingBoxesOnImage([
    BoundingBox(x1=box_x1, x2=box_x2, y1=box_y1, y2=box_y2)
], shape=image.shape)

# Indy car augmentations pipeline for an image with a bounding box
seq = iaa.Sequential([
    iaa.GammaContrast(1.5), # add contrast
    iaa.MotionBlur(k=25, angle=[-45, 45]), # motion blur
    iaa.GaussianBlur(sigma=0.0), # gaussian blur
    iaa.MeanShiftBlur(), # meanshift blur
    iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
    iaa.Fliplr(p = 0.8) # apply horizontal flip
])

# apply augmentations
image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)


# Plot the initial and the augmented images with bounding boxes
# using helpers from imgaug package
side_by_side = np.hstack([
    bbs.draw_on_image(image, size=2), # blend the original image with bounding box
    bbs_aug.draw_on_image(image_aug, size=2) # blend the augmented image with bounding box
])

# Plot with matplotlib imshow()
fig, ax = plt.subplots(figsize=(10, 7))
ax.axis('off')
plt.title('Augmentations for bounding boxes')
ax.imshow(side_by_side)
plt.show()
