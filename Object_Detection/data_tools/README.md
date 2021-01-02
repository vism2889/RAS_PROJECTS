# Various tools to help with collecting and augmenting training data.

## Indy Augmentation Script
### The `batch_augmentation.py` script was written using python3 and the imgaug library to generate training data by augmenting existing images with corresponding XML files with labels and bounding boxes.  The script takes a directory and performs a selection of random augmentation functions with arguments that have been chosen to simulate realistic motionBlur, camera perspective, lighting, and weather conditions that an indy car might experience while racing.


## Testing Augmentations
### The `augmentation_test.py` script allows for testing different augmentation functions and corresponding settings on a single image with output through matplotlib.

## Video Data Collection
### The `youtube_playlist_downloader.py` script can be used to download all the videos from a desired Youtube playlist.  In combination with `video_to_images.py`, collecting a large amount of training data and quickly should be much easier.

## Frame Grabbing
### The `video_to_images.py` script grabs image frames from a video file with a specified # of frames skipped over in between each frame grab.

## Data Cleaning
### The `dataCleaner.py` script takes a folder of images that have been filtered, and then filters the corresponding annotations files from the annotations folder.  Good removing unwanted images from a dataset based on visual inspection, and then automating the process of removing the corresponding annotations.
