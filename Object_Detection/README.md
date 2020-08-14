# See `frozen_models` for Indy Car Detector


# Indy Augmentation Script
### The `batch_augmentation.py` script was written using python3 and the imgaug library to generate training data by augmenting existing images with corresponding XML files with labels and bounding boxes.  The script takes a directory and performs a selection of random augmentation functions with arguments that have been chosen to simulate realistic motionBlur, camera perspective, lighting, and weather conditions that an indy car might experience while racing.


# Testing Augmentations
### The `augmentation_test.py` script allows for testing different augmentation functions and corresponding settings on a single image with output through matplotlib.
