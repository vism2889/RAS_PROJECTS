# Indy Car Detector

### I trained my detector using Gilbert Tanner's tutorial [here](https://gilberttanner.com/blog/installing-the-tensorflow-object-detection-api) to setup tensorflow's object detection api, and his tutorial [here](https://gilberttanner.com/blog/creating-your-own-objectdetector) to train the detector.

### The detector was trained using transfer learning and the 'faster_rcnn_inception_v2_coco_2018_01_28' model that was indicated in the tutorial.

### the included files are: 'indycar_frozen_inference_graph.pb' and 'indycar_labelmap.pbtxt' whose file extensions can be plugged into the code from [here](https://gilberttanner.com/blog/creating-your-own-objectdetector) to run the indy car detector.


# TODO:
- Train using a faster model, current one runs very slow on video files, or frames from a camera.
- Use image augmentation to increase amount of training data.
- Setup and test performance on GPU
