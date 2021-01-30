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
path_to_video = '/home/ubuntu/data/originals/sebastian_vettel.mp4'

# Path to directory to output frames and video (this folder will be created)
output_from_video_dir = '/home/ubuntu/data/frames_output/sebastian_vettel'

if os.path.exists(output_from_video_dir):
    shutil.rmtree(output_from_video_dir)

os.mkdir(output_from_video_dir)
os.chdir(output_from_video_dir)

# ------------ convert to frames -------------
vidcap = cv2.VideoCapture(path_to_video)

images = []

def getFrame(sec, count):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()

    if hasFrames:
        images.append(str(count)+".jpg")
        cv2.imwrite(images[-1], image)

sec = 0
frameRate = vidcap.get(cv2.CAP_PROP_FPS)

if vidcap.get(cv2.CAP_PROP_FRAME_COUNT) > 2000:
    frame_num = 2000
else:
    frame_num = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

print("Converting to Frames")
for i in tqdm(range(frame_num)):
    sec = sec + 1.0/frameRate
    sec = round(sec, 2)
    getFrame(sec, i)

# ----------- rescale ----------
def rescale_images(directory, size):
    print("Rescaling Images")
    for img in tqdm(os.listdir(directory)):
        im = Image.open(img)
        im_resized = im.resize(size, Image.ANTIALIAS)
        im_resized.save(img)

rescale_images(output_from_video_dir, (800,600))

# --------- convert back to video -------------
image_folder = output_from_video_dir
video_name = output_from_video_dir + '_rescaled.avi'

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, frameRate, (width,height))

print("Converting to Video")
for image in tqdm(images):
    video.write(cv2.imread(os.path.join(image_folder, image)))

print("All Done")
cv2.destroyAllWindows()
video.release()
