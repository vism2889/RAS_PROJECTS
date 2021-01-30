#! /usr/bin/env python
# AUTHORS: Noah Gasparro
# DATE: 01/11/2021
# FILENAME: LabelBox_to_FairMOT_annotations.py
#
###############################################################################
# INFO:
# - Converts annotations from labelbox.com into annoations usable with fairMOT network



import csv
from tqdm import tqdm
import os
# fairMOT format: "class id x_center/img_width y_center/img_height w/img_width h/img_height"

def format_data(img_height, img_width, datafile):
    # read in data file
    file = open(datafile)
    reader = csv.reader(file, delimiter=',')

    count = 0
    items = []
    matchers = ['featureId', 'top', 'left', 'height', 'width']
    frame_numbers = []
    car_id = {}
    n = 1
    for line in reader:
        new_items = [] # clear new_items array

        # pulls out important data from file based on matchers array
        matching = [s for s in line if any(xs in s for xs in matchers)]

        # segments data into a array of arrays which are of the size of the matchers array
        step_size = len(matchers)
        for i in range(0, len(matching), step_size):
            new_items.append(matching[i:i+step_size])

        # array that will get added to total array with fairMOT formatted data
        new_array = [['' for x in range(len(new_items[0]))] for y in range(len(new_items))]

        # crop only the important data to use later
        for i in range(len(new_items)):
            for j in range(len(new_items[0])):
                new_items[i][j] = new_items[i][j].split(matchers[j],1)[1]
                # removes all double quotes, colons and brackets
                new_items[i][j] = new_items[i][j].replace(':', '')
                new_items[i][j] = new_items[i][j].replace('"', '')
                new_items[i][j] = new_items[i][j].replace('}', '')

            feature_id = str(new_items[i][0]) # ensure that the feature_id is a string
            # each feature id has a number corresponding to it for identifying different cars
            if not feature_id in car_id:
                car_id[feature_id] = n
                n += 1

            vehicle_id = car_id[feature_id] # car identification number
            top = float(new_items[i][1]) # top of bounding box
            left = float(new_items[i][2]) # left x_value of bounding box
            height = float(new_items[i][3]) # height of bounding box
            width = float(new_items[i][4]) # width of bounding box

            # find new parameters for fairMOT format
            x_center = left + width/2
            y_center = top + height/2

            # populate new_array with fairMOT
            new_array[i][0] = vehicle_id
            new_array[i][1] = x_center/img_width
            new_array[i][2] = y_center/img_height
            new_array[i][3] = width/img_width
            new_array[i][4] = height/img_height

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
def output_annotations(items, train_size, test_size, frame_numbers):
    print("Making annotation files")

    # make annotations folder structure if it doesn't exist
    dirs = ['labels_with_ids', 'labels_with_ids/train', 'labels_with_ids/val']
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            os.system("rm -r "+dir)
            os.makedirs(dir)

    count = 0
    for item in tqdm(items): # for each image
        frame = frame_numbers[count]
        if count < train_size:
            filename = dirs[1]+'/'+str(frame)+'.txt'
        else:
            filename = dirs[2]+'/'+str(frame)+'.txt'

        with open(filename, 'w') as f:
            for car in item:
                line = "0 {:d} {:.6f} {:.6f} {:.6f} {:.6f}".format(car[0], car[1], car[2], car[3], car[4])
                f.write(line+"\n")
        count += 1


if __name__ == '__main__':

    img_height = float(input("Enter height of images: "))
    img_width  = float(input("Enter width of images: "))

    datafile = input("Enter data file: ")
    while os.path.isfile(datafile) is False:
        datafile = input("Not a valid file. Try again: ")

    train_percent = float(input("Enter the percent of the data that will be used for training: "))
    while train_percent > 100 or train_percent < 1:
        train_percent = float(input("Enter a percentage between 1 and 100: "))


    items, count, frame_numbers = format_data(img_height, img_width, datafile)
    print("Number of lines: " + str(count))

    print(items[0]) # first index = image, second index = car instance, third index = item in instance (i.e. fairMOT format item)

    # delete frames not needed (these frames include text that are not ideal for training)
    # delete_frames = 0
    # for frame in frame_numbers:
    #     if frame < 220:
    #         delete_frames += 1
    # items = items[delete_frames:]
    # frame_numbers = frame_numbers[delete_frames:]

    # split data up into training and testing data
    item_length = len(items)
    if item_length == len(frame_numbers):
        print("Array Lengths match")
        print(item_length)
    else:
        raise ValueError('frame_numbers and items array length should match')

    train_size = int(item_length * (train_percent/100))
    test_size = item_length - train_size

    output_annotations(items, train_size, test_size, frame_numbers) # make annotation text file for each image
