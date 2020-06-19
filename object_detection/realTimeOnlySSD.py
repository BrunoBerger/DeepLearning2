# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from datetime import datetime
import numpy as np
import imutils
import time
import cv2
import os
import csv
import functools

from geolocation import gps

class detectedObject(object):
    def __init__(self, name, posInFrame, timestamp, location, confidence):
        self.name = name
        self.pos = posInFrame
        self.time = timestamp
        self.location = location
        self.conf = confidence

def logDetection(filePath, newObj):
    # log the detections into a new csv file
    with open(filePath,'a') as file:
        reader = csv.reader(file, delimiter=',')
        file.write("{},{:.2f} %,{},{},{}".format(newObj.name,
                                                 newObj.conf*100,
                                                 newObj.location[0],
                                                 newObj.location[1],
                                                 newObj.time))
        file.write("\n")
    print("Logging ", newObj.name)


def main(args, run_flag, output_flag):
    # change print behaviour to always flush the sys.stdout buffer
    global print
    print = functools.partial(print, flush=True)

    ### SETUP
    print("Loading a SSD-MobileNet")

    basePath = args["path"]
    net = cv2.dnn.readNetFromCaffe(basePath + "/MobileNetSSD_deploy.prototxt.txt",
    basePath + "/MobileNetSSD_deploy.caffemodel")

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "monitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # set path to a new csv file for logs
    curTime = datetime.now()
    curTimeStr= curTime.strftime("%Y-%m-%d_%H-%M-%S")
    filePath = "logs/" + curTimeStr + ".csv"

    # create and position the output-window on the screen
    if output_flag.value == True:
        print("Starting in Reder MOde")
        cv2.namedWindow("Object Detection Running")
        cv2.moveWindow("Object Detection Running", 300,300)

    ### DETECTION

    # Start webcam-capture
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(0.5)
    fps = FPS().start()

    # to later filter out redundant objects
    objectBuffer = []

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

                # get info about the detected object
                name = CLASSES[idx]
                posInFrame = [startX, startY]
                timestamp = datetime.now()
                location = gps.givePosition()

                # draw the prediction on the frame
                label = "{} : {:.2f}%".format(name,
                    confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                # check if the new object is too similar to previous ones
                newObj = detectedObject(name, posInFrame, timestamp, location, confidence)
                for oldObj in objectBuffer:
                    if oldObj.name == newObj.name:

                        # get last time this type was logged
                        timeDeltas = []
                        for oldObj in objectBuffer:
                            timeDelta = (newObj.time - oldObj.time).total_seconds()
                            timeDeltas.append(timeDelta)

                        # get how much this object has moved on the screen
                        posDeltas = []
                        for oldObj in objectBuffer:
                            posDelta = newObj.pos[0] - oldObj.pos[0]
                            posDelta = abs(posDelta)
                            posDeltas.append(posDelta)
                        # print(name, "moved this ",posDelta, "pixels")

                        if not timeDeltas or posDeltas:
                            logDetection(filePath, newObj)
                        elif min(timeDeltas) > 5 or min(posDeltas) > 100:
                            logDetection(filePath, newObj)

                    else:
                        logDetection(filePath, newObj)
                objectBuffer.append(newObj)

                print("Buffer is this long: ", len(objectBuffer))
                objectsInBuffer = [n.name for n in objectBuffer]
                print("Detections in buffer: ", objectsInBuffer)

        if len(objectBuffer) > 8:
                del(objectBuffer[0:1])

        # show the output frame, or create a new window if destroyed
        if output_flag.value == True:
            cv2.imshow("Object Detection Running", frame)

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
    objectBuffer.clear()
    cv2.destroyAllWindows()
    vs.stop()
