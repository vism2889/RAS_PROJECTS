#! /usr/bin/env python
# AUTHORS: Thomas Detlefsen, Noah Gasparro, Morgan Visnesky
# DATE: 01/11/2021
# FILENAME: rescale_video.py
#
###############################################################################
# INFO:
# - Rescales a video


from PIL import Image
import cv2
import os
import shutil
import argparse
from tqdm import tqdm

# Path to video to rescale
path_to_video = '/home/ubuntu/Videos_data/ChristianBrooksPassing.mp4'

# Path to directory to output frames and video (this folder will be created)
output_from_video_dir = '/home/ubuntu/video_to_image_exports/'

if os.path.exists(output_from_video_dir):
    shutil.rmtree(output_from_video_dir)

os.mkdir(output_from_video_dir)

# ------------ convert to video -------------
vidcap = cv2.VideoCapture(path_to_video)

images = []

def getFrame(sec, count):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()

    if hasFrames:
        images.append(output_from_video_dir+str(count)+".jpg")
        cv2.imwrite(images[-1], image)

sec = 0
frameRate = vidcap.get(cv2.CAP_PROP_FPS)

print("Converting to Frames")
for i in tqdm(range(int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))):
    sec = sec + 1.0/frameRate
    sec = round(sec, 2)
    getFrame(sec, i)

# ----------- rescale ----------
def rescale_images(directory, size):
    print("Rescaling Images")
    for img in tqdm(os.listdir(directory)):
        im = Image.open(directory+img)
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(directory+img)

rescale_images(output_from_video_dir, (800,600))

# --------- convert back to video -------------
image_folder = output_from_video_dir
video_name = output_from_video_dir + 'rescaled_video.avi'

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, frameRate, (width,height))

print("Converting to Video")
for image in tqdm(images):
    video.write(cv2.imread(os.path.join(image_folder, image)))

print("All Done")
cv2.destroyAllWindows()
video.release()
