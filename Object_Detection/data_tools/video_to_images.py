#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 08/16/2020
# FILENAME: video_to_images.py
#
###############################################################################
# INFO:
# - Script to convert video to images as a means for gathering training data for object detection
# - uses detecto library
#
# TODO:
#
#


from detecto.utils import split_video
import os

def generateNewFilename(oldName):
    folderName = oldName[:-4]
    name = folderName.replace(" ","_")
    return name 

# path to directory with all videos in it
path_to_video_folder = '/home/morgan/Videos_data/' 

# path to directory in which you wish to output video frame folders to
output_from_video_dir = '/home/morgan/video_to_image_exports/'


video_list = os.listdir(path_to_video_folder)
frame_skip = 10
output_prefix = 'racecar_'

# creates output folder if doesn't exist
if not os.path.exists(output_from_video_dir):
    os.mkdir(output_from_video_dir)

for i in range(len(video_list)):
    name = generateNewFilename(video_list[i])
    print('generating images for: ' + name)
    vid_path = path_to_video_folder + video_list[i]
    frame_output_path = output_from_video_dir + "frame_output_" + name
    
    # creates output folder if doesn't exist
    if not os.path.exists(frame_output_path):
        os.mkdir(frame_output_path)
    
    split_video(vid_path, frame_output_path, prefix=output_prefix, step_size=frame_skip)

