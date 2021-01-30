import cv2
from tqdm import tqdm # PROGESS BAR!!!
import os

dir_in = './'
dir_out = './'
video_name = 'vid'

# Read files from directory
files = [f for f in os.listdir(dir_in) if os.path.isfile(os.path.join(dir_in, f))]

# Clean up files
files.sort()

# Get width and height of video
img = cv2.imread(dir_in+files[0])
height, width, layers = img.shape
size = (width,height)

# Instantiate video writer
video = cv2.VideoWriter(dir_out+vid+'.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 24, (width,height))

# Write to file (w/ progress bar!!!)
for image in tqdm(files):
    video.write(cv2.imread(os.path.join(dir_in, image)))

video.release()
