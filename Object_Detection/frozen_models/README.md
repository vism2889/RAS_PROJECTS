# Indy Car Detector

### I trained a handful of different detectors using Gilbert Tanner's tutorial [here](https://gilberttanner.com/blog/installing-the-tensorflow-object-detection-api) to setup tensorflow's object detection api, and his tutorial [here](https://gilberttanner.com/blog/creating-your-own-objectdetector) to train the detectors.

### Detectors were trained with:
*  'faster_rcnn_inception_v2_coco_2018_01_28' (model that was indicated in the tutorial)
*  'ssd_inception_v2_coco_2017_11_17'

### Each folder includes the files: 'indycar_frozen_inference_graph.pb' and 'indycar_labelmap.pbtxt' which once downloaded, thier file extensions can be plugged into the code in the jupyter notebook [here](https://gilberttanner.com/blog/creating-your-own-objectdetector) to run the different indy car detectors.


# Detector in action (faster_rcnn_inception_v2_coc_2018_01_28):
<p float = "left">
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector1.png" width="200" />
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector2.png" width="200" />
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector3.png" width="200" />
  <img src="https://github.com/vism2889/RAS_PROJECTS/blob/master/images/indycar_detector4.png" width="200" />
</p>

### TODO: upload other models, compare and visualize accuracy and speed.