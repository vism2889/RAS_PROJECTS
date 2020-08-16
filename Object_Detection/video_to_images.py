#! /usr/bin/env python
# AUTHOR: Morgan Visnesky
# DATE: 08/16/2020
# FILENAME: video_to_images.py
#
###############################################################################
# INFO:
# - Script to convert video to images as a means for gathering training data for object detection
# - uses detecto library


from detecto.utils import split_video
import os



vidPath = '/home/morgan/Downloads/testVid.mp4'
frameOutputPath = '/home/morgan/Downloads/testVidFrames2/'
frameSkip = 10


# checks to see if output directory exists, if not it is created
if not os.path.exists(frameOutputPath):
    os.mkdir(frameOutputPath)



#split_video('video file path', 'image save path', frame size)
split_video(vidPath, frameOutputPath, step_size=frameSkip)