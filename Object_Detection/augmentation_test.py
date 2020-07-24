#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 07/23/2020
# FILENAME: augmentation_test.py
#
###############################################################################
# INFO:
# - Script to augment a single prelabeled image with bounding boxes.
# - Uses python3 and imgaug library.
# - Used to test output of augmentations before using batch augmenter
# - Assumes only one label is being used in our case 'racecar'

import os
import math
import imageio
from imgaug import augmenters as iaa
#from imgaug import
from matplotlib import pyplot as plt
import numpy as np
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import xml.etree.ElementTree as ET
from PIL import Image



def getAllBoundingBoxes(filename,root):
    # gets and returns all bounding boxes from an unaffected image
    allBoxCoords = []
    for child in root:
        if child.tag == 'object':
            newCoords = []
            for i in range(4):
                #print(child[4][i].text)
                newCoords.append(int(child[4][i].text))
            #print(newCoords)
            allBoxCoords.append(newCoords)
    return allBoxCoords

def getAugBoundingBoxes(augmentedBoundingBox):
    # grabs values from augmented bounding boxes
    a = augmentedBoundingBox
    x1 = a.x1
    y1 = a.y1
    x2 = a.x2
    y2 = a.y2
    return (x1,y1,x2,y2)

def main():
    filename = '/Users/morganvisnesky/RAS_PROJECTS/images/images_xml_test/racecar003'
    xml = '.xml'
    jpg = '.jpg'
    jpeg = '.jpeg'
    png = '.png'
    tree = ET.parse(filename + xml)
    root = tree.getroot()
    image = imageio.imread(filename + jpg)



    # gets all bounding boxes from a certain file and creates bbs with them
    allboxes = getAllBoundingBoxes(filename + xml,root)
    allbbs = []
    for box in allboxes:
        box_x1 = box[0]
        box_y1 = box[1]
        box_x2 = box[2]
        box_y2 = box[3]
        newBox = BoundingBox(x1=box_x1, x2=box_x2, y1=box_y1, y2=box_y2)
        allbbs.append(newBox)

    # store all bounding boxes
    bbs = BoundingBoxesOnImage(allbbs, shape=image.shape)

    # augmentation sequence
    #
    seq = iaa.Sequential([
        iaa.GammaContrast(1.5), # add contrast
        iaa.MotionBlur(k=25, angle=[-45, 45]), # motion blur
        #iaa.GaussianBlur(sigma=0.0), # gaussian blur
        #iaa.MeanShiftBlur(), # meanshift blur
        #iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
        #iaa.Affine(translate_percent={"y": 0.2}, scale=1.2),
        iaa.Fliplr(p = 1.0) # apply horizontal flip
    ])

    # apply augmentations
    image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

    # creates new augmented bounding boxes
    aug_boxes = []
    for i in range(len(bbs_aug.bounding_boxes)):
        aug_boxes.append(getAugBoundingBoxes(bbs_aug.bounding_boxes[i]))

    # add bounding boxes to images
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

if __name__ == '__main__':
    print("Generating Augment....")
    main()
