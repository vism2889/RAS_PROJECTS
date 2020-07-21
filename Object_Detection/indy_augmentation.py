#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 07/15/2020
# FILENAME: indy_augmentation.py
#
###############################################################################
# INFO:
# - Script to augment a set of prelabeled images with bounding boxes.
# - Uses python3 and imgaug library.
# - Assumes given directory is full of image files with names that match corresponding XML
#   files names. EX: 'racecar004.jpg' & 'racecar004.xml'
#
###############################################################################

import os
import math
import imageio
from imgaug import augmenters as iaa
from matplotlib import pyplot as plt
import numpy as np
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import xml.etree.ElementTree as ET

def getBoundingBox(filename):
    # parses XML file for bounding box coordinates for single object and box
    # ** accomodate for multiple bounding boxes
    root = ET.parse(filename).getroot()
    coords = []
    for i in range(4):
        val = int(root[6][4][i].text)
        coords.append(val)
    return coords

def getAllBoundingBoxes(filename,root):
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
    a = augmentedBoundingBox
    x1 = a.x1
    y1 = a.y1
    x2 = a.x2
    y2 = a.y2
    return (x1,y1,x2,y2)


def getAllFiles(directoryPATH,filename):
    # makes list of all files in chosen directory
    # Example directoryPath = '/Users/morganvisnesky/RAS_PROJECTS/folder_holding_images'
    files = os.listdir(directoryPATH)
    folderSize = len(files)
    fileNames = []
    for i in range(folderSize//2):
        numLabel = "{:0>3d}".format(i+1)
        currFile = filename + numLabel
        fileNames.append(currFile)
    return fileNames

def generateNewImage(newFilename,img_aug):
    # generates new image file and saves in chosen directory
    imageio.imwrite(newFilename, img_aug)
    return 42

def generateNewXML(oldFilename, newFilename):
    # generates new xml file and saves in chosen directory
    linelist = []
    with open(oldFilename + ".xml") as f:
        with open(newFilename + ".xml", "w") as f1:
            for line in f:
                linelist.append(line)
                f1.write(line)
    return linelist

def generateNewFilename(filename):
    # generates new file name: EX: old = 'racecar004', new = 'racecar004_AUG_1'
    # if augmented a second time increment 'AUG_1' to be 'AUG_2, AUG_3...AUG_N'
    # N being the nth time a single image has been run through the augmenter
    return 42

def imageFileEXT(directoryPATH, filename):
    # finds image file matching name and determines correct extension
    jpg = '.jpg' # add logic for .jpeg and .png
    jpeg = '.jpeg'
    png = '.png'
    correctFile = ''
    files = os.listdir(directoryPATH)
    for file in files:
        if (file == filename + jpg) or (file == filename + jpeg) or (file == filename + png):
            correctFile = file
            break
    return correctFile

def xmlFileEXT(filename):
    xml = '.xml'
    newFilename = filename + xml
    return newFilename

def augmentationSequence():

    # holds all possible augmentors
    possibleAugs = [
        iaa.GammaContrast(1.5), # add contrast

        # motion blur, use between 25 and 155 for k to get results accurate to fast indy-car
        iaa.MotionBlur(k=155, angle=[-45, 45]),

        #iaa.GaussianBlur(sigma=0.0), # gaussian blur
        iaa.MeanShiftBlur(), # meanshift blur
        iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
        iaa.Affine(translate_percent={"y": 0.2}, scale=1.2),
        iaa.Fliplr(p = 0.8) # apply horizontal flip
    ]

    chosenAugs = []
    randomSize = random.randint(len(possibleAugs//2), len(possibleAugs))
    for i in range(randomSize):
        randomAugNum = random.randint(0, len(possibleAugs))
        chosenAugs.append(possibleAugs[randomAugNum])
    seq = iaa.Sequential(chosenAugs)
    '''
    seq = iaa.Sequential([
        iaa.GammaContrast(1.5), # add contrast

        # motion blur, use between 25 and 155 for k to get results accurate to fast indy-car
        iaa.MotionBlur(k=155, angle=[-45, 45]),

        #iaa.GaussianBlur(sigma=0.0), # gaussian blur
        iaa.MeanShiftBlur(), # meanshift blur
        iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
        iaa.Affine(translate_percent={"y": 0.2}, scale=1.2),
        iaa.Fliplr(p = 0.8) # apply horizontal flip
    ])
    '''
    return seq

def performAugment(imageFilename,boundingBox):
    xmlbox = boundingBox
    box_x1 = xmlbox[0]
    box_y1 = xmlbox[1]
    box_x2 = xmlbox[2]
    box_y2 = xmlbox[3]
    bbs = BoundingBoxesOnImage([
        BoundingBox(x1=box_x1, x2=box_x2, y1=box_y1, y2=box_y2)
    ], shape=image.shape)

    seq = augmentationSequence()
    '''
    seq = iaa.Sequential([
        iaa.GammaContrast(1.5), # add contrast

        # motion blur, use between 25 and 155 for k to get results accurate to fast indy-car
        iaa.MotionBlur(k=155, angle=[-45, 45]),

        #iaa.GaussianBlur(sigma=0.0), # gaussian blur
        iaa.MeanShiftBlur(), # meanshift blur
        iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
        iaa.Affine(translate_percent={"y": 0.2}, scale=1.2),
        iaa.Fliplr(p = 0.8) # apply horizontal flip
    ])
    '''
    # apply augmentations
    image_aug, bbs_aug = seq(image=imageFilename, bounding_boxes=bbs)

    return [image_aug, bbs_aug]

def indyAugmenter(filename, direcotryPATH):
    filenames = getAllFiles()
    for file in filenames:
        imageFile = imageFileEXT(directoryPATH, file)
        xmlFile = xmlFileEXT(file)
        boundingBox = getBoundingBox(xmlFile)
        (image_aug, bbs_aug) = performAugment(imageFile, boundingBox)
        # save image
        # save xml file with new coordinates


    return 42

def updateXML(filename, root, tree, newFilename, augboxes):
    allBoxCoords = augboxes#getAllBoundingBoxes(filename,root)
    xmin = 0
    for object in root.iter('xmin'):
            print(object.tag, object.attrib)
            object.text = str(math.floor(allBoxCoords[xmin][0]))
            xmin += 1
    ymin = 0
    for object in root.iter('ymin'):
            print(object.tag, object.attrib)
            object.text = str(math.floor(allBoxCoords[ymin][1]))
            ymin += 1

    xmax = 0
    for object in root.iter('xmax'):
            print(object.tag, object.attrib)
            object.text = str(math.floor(allBoxCoords[xmax][2]))
            xmax += 1
    ymax = 0
    for object in root.iter('ymax'):
            print(object.tag, object.attrib)
            object.text = str(math.floor(allBoxCoords[ymax][3]))
            ymax += 1

    tree.write(newFilename)







def main():
    PATH = '/Users/morganvisnesky/RAS_PROJECTS/Object_Detection/images_xml'
    newPATH = '/Users/morganvisnesky/RAS_PROJECTS/Object_Detection/images_xml_AUG'
    try:
        os.mkdir(newPATH)
    except OSError:
        print ("Creation of the directory %s failed" % newPATH)
    else:
        print ("Successfully created the directory %s " % newPATH)

    xml = '.xml'
    jpg = '.jpg' # add logic for .jpeg and .png
    jpeg = '.jpeg'
    png = '.png'
    all = getAllFiles(PATH,'racecar')
    print(all)
    for i in range(len(all)):
        filename = all[i]
        tree = ET.parse(PATH + '/' +filename+xml)
        root = tree.getroot()
        image = imageio.imread(PATH + '/' + imageFileEXT(PATH,filename))

        allboxes = getAllBoundingBoxes(PATH + '/' +filename + xml,root)
        allbbs = []
        for box in allboxes:
            print(box)
            box_x1 = box[0]
            box_y1 = box[1]
            box_x2 = box[2]
            box_y2 = box[3]

            newBox = BoundingBox(x1=box_x1, x2=box_x2, y1=box_y1, y2=box_y2)

            allbbs.append(newBox)

        bbs = BoundingBoxesOnImage(allbbs, shape=image.shape)
        print(bbs)

        seq = iaa.Sequential([
            iaa.GammaContrast(1.5), # add contrast

            # motion blur, use between 25 and 155 for k to get results accurate to fast indy-car
            iaa.MotionBlur(k=155, angle=[-45, 45]),

            #iaa.GaussianBlur(sigma=0.0), # gaussian blur
            iaa.MeanShiftBlur(), # meanshift blur
            iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
            iaa.Affine(translate_percent={"y": 0.2}, scale=1.2),
            iaa.Fliplr(p = 0.8) # apply horizontal flip
        ])

        # apply augmentations
        image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

        # update new xml file
        aug_boxes = []
        for i in range(len(bbs_aug.bounding_boxes)):
            aug_boxes.append(getAugBoundingBoxes(bbs_aug.bounding_boxes[i]))
            print(getAugBoundingBoxes(bbs_aug.bounding_boxes[i]))
        print(aug_boxes)
        updateXML(PATH + '/' + filename+xml, root,tree,newPATH + '/'+filename+'_AUG_1'+xml,aug_boxes)
        generateNewImage(newPATH + '/'+filename+'_AUG_1'+png,image_aug)


main()

"""
#############################
# Tests for functionality
#############################
filename = 'racecar017'
xml = '.xml'
jpg = '.jpg' # add logic for .jpeg and .png
jpeg = '.jpeg'
png = '.png'
# use imageio library to read the image (alternatively you can use OpenCV cv2.imread() function)
tree = ET.parse(filename+xml)
root = tree.getroot()
image = imageio.imread('racecar004.jpg')
#xmlbox = getAllBoundingBoxes(filename + xml,root)


# gets all bounding boxes from a certain file and creates bbs with them
allboxes = getAllBoundingBoxes(filename + xml,root)
allbbs = []
for box in allboxes:
    print(box)
    box_x1 = box[0]
    box_y1 = box[1]
    box_x2 = box[2]
    box_y2 = box[3]

    newBox = BoundingBox(x1=box_x1, x2=box_x2, y1=box_y1, y2=box_y2)

    allbbs.append(newBox)

bbs = BoundingBoxesOnImage(allbbs, shape=image.shape)
print(bbs)

# Initialize the bounding box for the original image
# using helpers from imgaug package
'''
bbs = BoundingBoxesOnImage([
    BoundingBox(x1=box_x1, x2=box_x2, y1=box_y1, y2=box_y2)
], shape=image.shape)
'''
# Indy car augmentations pipeline for an image with a bounding box
# **make function to randomize arguments to augmenters
seq = iaa.Sequential([
    iaa.GammaContrast(1.5), # add contrast

    # motion blur, use between 25 and 155 for k to get results accurate to fast indy-car
    iaa.MotionBlur(k=155, angle=[-45, 45]),

    #iaa.GaussianBlur(sigma=0.0), # gaussian blur
    iaa.MeanShiftBlur(), # meanshift blur
    iaa.Affine(translate_percent={"x": 0.1}, scale=0.8), # translate the image
    iaa.Affine(translate_percent={"y": 0.2}, scale=1.2),
    iaa.Fliplr(p = 0.8) # apply horizontal flip
])

# apply augmentations
image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

# update new xml file
aug_boxes = []
for i in range(len(bbs_aug.bounding_boxes)):
    aug_boxes.append(getAugBoundingBoxes(bbs_aug.bounding_boxes[i]))
    print(getAugBoundingBoxes(bbs_aug.bounding_boxes[i]))
print(aug_boxes)
updateXML(filename+xml, root,filename+'_AUG_1'+xml,aug_boxes)
generateNewImage(filename+'_AUG_1'+png,image_aug)

#print(generateNewXML('racecar004', 'racecar004_AUG_1'))
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
"""
