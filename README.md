# Course
- https://blog.csdn.net/weixin_45921929/article/details/128656286

# This repository integrates the following functions

1. Using yolov7+tensorrt to achieve target detection

2. Index available GPUs in a multi-GPU environment

3. In a multi-threaded environment, use opencv to put/get pictures into the queue

4. Save the detection pictures and results as jpg and xml to facilitate subsequent iterative training

   

### Installation

1.Recommended to use the ubuntu system for operation, and the software configuration is as follows:

 - ubuntu20.04
 - cuda11.2
 - cudnn8.4.0
 - tensorrt8.4.3.1
 - python3.7
 - pytorch1.10.0
 - torchvision0.11.0

2.Download this repository

```bash
git clone https://github.com/ZhijunLStudio/yolov7_tensorrt_opencv_queue.git
```

3.Install dependent libraries

```sh
pip install -r requirements.txt
```



## Quick Start

1.Modify the detect.py file

```python
# According to your own model and camera information, modify 1, 2, 3
# 1. Put the name of the tensorrt engine under the model folder
trt_name = "best.engine"
# 2. rtsp address, if you are using a USB camera or other onboard camera, you can change it to 0 (without quotation marks)
RtspUrl = "rtsp://admin:admin@20.21.43.104:554/Streaming/Channels/101"
# 3. Automatically generate xml configuration - tag dictionary, need to follow {"configured folder name": {0: "label 1", 1: "label 2", 2: "label 3"...}} configure
label_dict = {'person': {0: 'person'}}
```

2.Run the detect.py file

```sh
python detect.py
```



 ## Reference
 - https://github.com/Monday-Leo/YOLOv7_Tensorrt
