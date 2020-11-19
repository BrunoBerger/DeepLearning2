# import needed modules
import cv2
import os
import argparse
import multiprocessing
import sys

# make realative paths work, regardless of cwd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from UI import interface


def main():
    print("Hello", os.getlogin() + ", lets get started!")

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.9,
        help="minimum probability to filter weak detections")
    ap.add_argument("-p", "--path", required=False, default="object_detection/MobileNetSSD",
        help="base path to models directory")
    args = vars(ap.parse_args())

    # to control and track threads
    run_flag = multiprocessing.Value('I', True)
    all_processes = []

    # Start Tkinter window with
    interface.optionWindow(args, run_flag, all_processes)

    # close loose threads
    run_flag.value = False
    for process in all_processes:
        process.join()

    print("Processes Terminated")
    print("[Done]")

if __name__ == "__main__":
   main()
