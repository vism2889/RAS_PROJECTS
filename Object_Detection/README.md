# Indy Car Detector

### I trained my detector using Gilbert Tanner's tutorial [here](https://gilberttanner.com/blog/installing-the-tensorflow-object-detection-api) to setup tensorflow's object detection api, and his tutorial [here](https://gilberttanner.com/blog/creating-your-own-objectdetector) to train the detector.

### The detector was trained using transfer learning and the 'faster_rcnn_inception_v2_coco_2018_01_28' model that was indicated in the tutorial.

### The included files are: 'indycar_frozen_inference_graph.pb' and 'indycar_labelmap.pbtxt' whose file extensions can be plugged into the code from [here](https://gilberttanner.com/blog/creating-your-own-objectdetector) to run the indy car detector.


# Detector in action:
<p float = "left">
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector1.png" width="200" />
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector2.png" width="200" />
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector3.png" width="200" />
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector4.png" width="200" />
</p>

# Indy Augmentation Script
### Th `indy_augmentation.py` script was written using python3 and the imgaug library to generate training data by augmenting existing images with corresponding XML files with labels and bounding boxes.  The script takes a directory and performs a selection of random augmentation functions with arguments that have been chosen to simulate realistic motionBlur, camera perspective, lighting, and weather conditions an indy car might experience.

# TODO:
- Train using a faster model, current one runs very slow on video files, or frames from a camera.
- Use image augmentation to increase amount of training data.
- Setup and test performance on GPU
