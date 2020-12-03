# DeepLearning2
A tool for detecting objects with locations and exporting them into Leaflet-maps
***
Object detection with a MobileNet-SSD detector, trained on the coco dataset.

Object Detection part was mostly influenced by [Ardian Rosebrock][pyimYOLO] from [PyImageSearch][pyimRT].

More information and all of taks to hand in for the DL2 module can be found in the [Wiki][wiki]

#

<img src="https://user-images.githubusercontent.com/43641701/100948748-de44e680-3508-11eb-9821-9ad86524c7e4.png" width="40%"></img> <img src="https://user-images.githubusercontent.com/43641701/100948556-637bcb80-3508-11eb-8b33-3f5973179ed4.png" width="20%"></img> <img src="https://user-images.githubusercontent.com/43641701/100948933-409de700-3509-11eb-88ab-cf79bce11519.png" width="35%"></img>

***

### Install and Use:
1. Make sure you are using at least [python 3.7][py] and have [pip][PIP] installed
2. Clone the repository on to your device
3. Navigate into the directory and run ```python -m pip install -r requirements.txt``` in your command line
4. Execute [main.py](https://github.com/BrunoBerger/DeepLearning2/blob/master/main.py)

***
This project is currently randomly generating the gps-info for demonstration purposes.  
If you want to use this in the real world,
you'll have to provide the programm with a way to get your real gps-data ![here](https://github.com/BrunoBerger/DeepLearning2/blob/02ddcdcfc1e97fccb647b40375d0004d2e6d8164/geolocation/gps.py#L4).


[pyimYOLO]: https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
[pyimRT]: https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/
[darknet]: https://pjreddie.com/darknet/yolo/
[wiki]: https://github.com/BrunoBerger/DeepLearning2/wiki

[py]: https://www.python.org/downloads/release/python-377/
[PIP]: https://pip.pypa.io/en/stable/installing/
