# import needed modules
import cv2
import os
import argparse
import tkinter
import threading

# import needed files
from object_detection import realTime
from GUI import windowPLUS

# Set current working dir to the one of main.py
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-y", "--type", required=False, default="yolo-coco",
    help="base path to YOLO directory")
ap.add_argument("-m", "--model", required=False, default="Tiny",
    help="chose between the yolov3 models 320 and Tiny")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
    help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

print("Hello ", os.getlogin(), "lets get started!")
cv2.namedWindow('wayCoolerWindow', flags= cv2.WINDOW_GUI_NORMAL)


detection = threading.Thread(target = realTime.main(args), daemon=True)
detection.start()
print("started Detection")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

# realTime.main(args)

print("done")
