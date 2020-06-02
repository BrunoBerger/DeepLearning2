# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from datetime import datetime
import numpy as np
import imutils
import argparse
import time
import cv2
import os
import csv

from geolocation import gps

### SETUP
def main(args, run_flag):
    ### SETUP

    # for shorter file-paths
    os.chdir("object_detection")

    print("Chosen Model Type:", args["type"])

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe("MobileNetSSD/MobileNetSSD_deploy.prototxt.txt",
        "MobileNetSSD/MobileNetSSD_deploy.caffemodel")

    ### DETECTION

    # Start webcam-capture
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
    fps = FPS().start()

    # set path to a new csv file for logs
    curTime = datetime.now()
    curTimeStr= curTime.strftime("%Y-%m-%d_%H-%M-%S")
    filePath = "../logs/" + curTimeStr + ".csv"

    # loop over the frames from the video stream
    # until run_flag == False, then thread runs out
    while run_flag.value:
        # grab the frame dimensions and convert it to a blob
        try:
            frame = vs.read()
            (h, w) = frame.shape[:2]
        except AttributeError:
            print("[ERROR] Please connect a Webcam to the PC")
            exit()
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)

		# pass the blob through the network and obtain the detections and
        # predictions
        start = time.time()
        net.setInput(blob)
        detections = net.forward()
        end = time.time()
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # detections, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

				# output the names of detected objets
                print(label,
                    " detected, with ", "%.2f" % confidence,
                    " confidence in {:.6f} seconds".format(end - start))

                # log the detections into a new csv file
                position = gps.givePosition()
                with open(filePath,'a') as file:
                    file.write("{},{},{},{},{}".format(label,
                        "%.2f" % confidence,
                        position[0], position[1],
                        datetime.now()))
                    file.write("\n")

        # show the output frame
        cv2.imshow("wayCoolerWindow", frame)
        # if the q key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break

    # update the FPS counter
    fps.update()
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
