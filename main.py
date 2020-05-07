# USAGE: execute main.py


from object_detection import realTime
from object_detection import test

import cv2
import threading
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


test.main("Bruno")

cv2.namedWindow('wayCoolerWindow', flags= cv2.WINDOW_GUI_NORMAL)

realTime.main()
# detection = threading.Thread(target = realTime.main)
# detection.start()


print("done")
