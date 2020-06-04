# import needed modules
import cv2
import os
import argparse
import multiprocessing

# import needed files
from object_detection import realTime
from object_detection import realTimeCombinedTest
from UI import interface
from geolocation import website


def main():
    print("Hello ", os.getlogin(), "lets get started!")

    # Set current working dir to the one of main.pyq
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-y", "--type", required=False, default="MobileNetSSD",
        help="base path to models directory (MobileNetSSD or yolo-coco)")
    ap.add_argument("-m", "--model", required=False, default="Tiny",
        help="chose between the yolov3 models 320 and Tiny")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
        help="minimum probability to filter weak detections")
    ap.add_argument("-t", "--threshold", type=float, default=0.3,
        help="threshold when applyong non-maxima suppression")
    args = vars(ap.parse_args())

    # to control and keep track of threads
    run_flag = multiprocessing.Value('I', True)
    all_processes = []

    # Start Tkinter window with
    interface.optionWindow(args, run_flag, all_processes)

    # close loose threads
    run_flag.value = False
    for process in all_processes:
        process.join()
    print("Process Terminated")
    print("done")

if __name__ == "__main__":
   main()
