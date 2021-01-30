#! /usr/bin/env python
# AUTHORS: Noah Gasparro, Morgan Visnesky
# DATE: 01/13/2021
# FILENAME: LabelBox_to_XML_annotations.py
#
###############################################################################
# INFO:
# - Converts annotations from labelbox.com into XML annotations

import csv
from tqdm import tqdm
import os

def format_data(img_height, img_width, datafile):
    # read in data file
    file = open(datafile)
    reader = csv.reader(file, delimiter=',')

    count = 0
    items = []
    matchers = ['title', 'top', 'left', 'height', 'width']
    frame_numbers = []
    for line in reader:
        new_items = [] # clear new_items array

        # pulls out important data from file based on matchers array
        matching = [s for s in line if any(xs in s for xs in matchers)]

        # segments data into a array of arrays which are of the size of the matchers array
        step_size = len(matchers)
        for i in range(0, len(matching), step_size):
            new_items.append(matching[i:i+step_size])

        # array that will get added to total array
        new_array = [['' for x in range(len(new_items[0]))] for y in range(len(new_items))]

        # crop only the important data to use later
        for i in range(len(new_items)):
            for j in range(len(new_items[0])):

                new_items[i][j] = new_items[i][j].split(matchers[j],1)[1]
                # removes all double quotes, colons and brackets
                new_items[i][j] = new_items[i][j].replace(':', '')
                new_items[i][j] = new_items[i][j].replace('"', '')
                new_items[i][j] = new_items[i][j].replace('}', '')

            top = float(new_items[i][1]) # top of bounding box
            left = float(new_items[i][2]) # left x_value of bounding box
            height = float(new_items[i][3]) # height of bounding box
            width = float(new_items[i][4]) # width of bounding box

            # populate new_array with [object_label, xmin ,ymin ,xmax ,ymax]
            new_array[i][0] = new_items[i][0]
            new_array[i][1] = left
            new_array[i][2] = top - height
            new_array[i][3] = left + width
            new_array[i][4] = top

        # append new items to total data array
        items.append(new_array)
        count += 1

        # pull out frame Number (double check that listed frame number is the same as the line)
        frame_number = ''
        for ele in line:
            if 'frameNumber' in ele:
                frame_number = ele
        frame_number = frame_number.split('frameNumber',1)[1]
        frame_number = frame_number.replace(':', '')
        frame_number = frame_number.replace('"', '')

        frame_numbers.append(int(frame_number))
    return items, count, frame_numbers

# outputs each set of image annotations to its own file as prescribed by fairMOT
def output_XML_annotations(annotation, fileName):
    print("Making annotation files")
    filename = 'XML_Annotations/racecar_'+fileName+'.txt'
    with open(filename, 'w') as f:
        f.write(annotation)
        f.close()


if __name__ == '__main__':

    dirs = ['XML_Annotations']
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            os.system("rm -r "+dir)
            os.makedirs(dir)

    x = format_data(720, 1280, 'labelBox_dataset.txt')

    cars = len(x[0])
    for j in range(cars):
        l = []
        strang1 = "<annotation>\n\t<name>racecar_"+str(x[2][j])+".jpg</name>"
        strang2 ='''<path>/home/parallels/Downloads/sample_dataset/Images/100th_127.jpg</path>
<source>
  <database>Unknown</database>
</source>
<size>
  <width>1280</width>
  <height>720</height>
  <depth>3</depth>
</size>
<segmented>0</segmented>'''
        strang = '''<annotation>
            <folder>Images</folder>
            <filename>{fileName}</filename>
            <path>/home/parallels/Downloads/sample_dataset/Images/100th_127.jpg</path>
            <source>
        	        <database>Unknown</database>
            </source>
            <size>
        	        <width>1280</width>
        	        <height>720</height>
        	        <depth>3</depth>
            </size>
            <segmented>0</segmented>'''
        strang = strang1 + strang2
        for k in range(len(x[0][j])):
            l.append(str(x[0][j][k][0]) + ' ')
            #print(str(l) + '\n')

            strang += "\n\t<object>\n\t<name>" + str(x[0][j][k][0]) + "</name>"
            strang += "\n\t\t<pose>Unspecified</pose>"
            strang += "\n\t\t<truncated>0</truncated>"
            strang += "\n\t\t<difficult>0</difficult>"
            strang += "\n\t\t<bndbox>"

            strang += "\n\t\t\t<xmin>" + str(x[0][j][k][1]) + "</xmin>"
            strang += "\n\t\t\t<ymin>" + str(x[0][j][k][2]) + "</ymin>"
            strang += "\n\t\t\t<xmax>" + str(x[0][j][k][3]) + "</xmax>"
            strang += "\n\t\t\t<ymax>" + str(x[0][j][k][4]) + "</ymax>"
            strang += "\n\t\t</bndbox>"
            strang += "\n\t</object>"
        strang += "\n</annotation>"
        output_XML_annotations(strang, str(x[2][j]))
