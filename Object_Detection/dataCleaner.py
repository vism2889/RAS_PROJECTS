# AUTHOR: Morgan Visnesky
# DATE: 11/15/2020
# FILENAME: dataCleaner.py
#
# DESCRIPTION:
#
# Takes a data set in the form of a folder of images and a folder of XML
# annotations.  The folder of images is assumed to be 'cleaned' in the sense
# that images not relevent to the use case have been removed.  The script will
# then find the matching xml files that correspond to the images filenames
# and copy them into a new annotations folder.
#
#


import os
from shutil import copyfile
imgFolderEXT = "/Users/morgan/Documents/indyDataSet_for_cleaning/test_imgs"
XMLFolderEXT = "/Users/morgan/Documents/indyDataSet_for_cleaning/test_xmls"
newXMLFolderEXT = "/Users/morgan/Documents/indyDataSet_for_cleaning/NEW_annotations"


listOfImageFiles = os.listdir(imgFolderEXT)
for i in range(len(listOfImageFiles)):
    listOfImageFiles[i] = listOfImageFiles[i][:-4]

for i in range(len(listOfImageFiles)):
    print(listOfImageFiles[i])

os.mkdir(newXMLFolderEXT)
listOfXmlFiles = os.listdir(XMLFolderEXT)
for i in range(len(listOfImageFiles)):
    XMLfileEXT = listOfImageFiles[i] + ".xml"
    dirr = newXMLFolderEXT + "/" + XMLfileEXT

    if XMLfileEXT in listOfXmlFiles:
        copyfile(XMLFolderEXT + "/" + XMLfileEXT, dirr)
