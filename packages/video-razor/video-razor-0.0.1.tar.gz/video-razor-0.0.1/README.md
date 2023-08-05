[![Build Status](https://travis-ci.com/5starkarma/face-smoothing.svg?branch=main)](https://travis-ci.com/5starkarma/face-smoothing) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Video Razor

1 | 2 | 3
:-------------------------:|:-------------------------:|:-------------------------:
![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-1.png?raw=true "Input image")  |  ![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-2.png?raw=true "Output image") |  ![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-3.png?raw=true "Output image")
4 | 5 | 6
![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-4.png?raw=true "Input image")  |  ![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-5.png?raw=true "Output image") |  ![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-6.png?raw=true "Output image")
7 | 8 | 9
![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-7.png?raw=true "Input image")  |  ![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-8.png?raw=true "Output image") |  ![alt text](https://github.com/5starkarma/video-razor/blob/master/data/examples/section-9.png?raw=true "Output image")
---

A package for slicing a video into N**2 sections. 

The original use-case was to process higher-definition videos, split up, through Deep Learning models. This allows for easier detection of smaller objects.

---
## Install
```
pip install video-razor
```

## Usage
The class input file name, output file name, and the cross sections you'd like to split the video in. e.g. `3` will produce an output of 9 videos - 3 horizontal, 3 vertical.

The output file name should **NOT** contain a suffix as this will be appended during processing.
```
input_file = 'data/input/sample.mp4'
output = 'data/output/out'
razor = VideoRazor(input_file, output, 3)
razor.slice()
```
