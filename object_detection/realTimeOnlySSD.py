# import the necessary packages
import csv
from datetime import datetime
import functools
import os
import time

import cv2
import imutils
from imutils.video import FPS
from imutils.video import VideoStream
import numpy as np

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

    ### SETUP ###
    #############
    basePath = args["path"]
    net = cv2.dnn.readNetFromCaffe(basePath + "/MobileNetSSD_deploy.prototxt.txt",
        basePath + "/MobileNetSSD_deploy.caffemodel")

    # for Cuda-GPU support
    try:
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    except:
        print("Using CPU")
        pass

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

    ### DETECTION ###
    #################

    # Start webcam-capture
    print("[INFO] starting video stream...")
    fps = FPS().start()
    # vs = VideoStream(src=0).start()



    vs = cv2.VideoCapture("./videos/video1.mp4")
    vs = cv2.VideoCapture("./videos/input.mp4")
    writer = None
    (W, H) = (None, None)
    # try to determine the total number of frames in the video file
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
            else cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        print("[INFO] {} total frames in video".format(total))
    # an error occurred while trying to determine the total
    # number of frames in the video file
    except:
        print("[INFO] could not determine # of frames in video")
        print("[INFO] no approx. completion time can be provided")
        total = -1



    time.sleep(0.5)

    # to later filter out redundant objects
    objectBuffer = []
    errorGuess = 0
    amout_of_individuals_detected = 0

    # loop over the frames from the video stream
    # until run_flag == False, then thread runs out
    while run_flag.value:
        # grab the frame dimensions and convert it to a blob
        try:
            grabbed, frame = vs.read()
            (h, w) = frame.shape[:2]
            fps.update()
            errorGuess += 1
        except AttributeError:
            # print("[ERROR] Please connect a Webcam to the PC")
            # exit()
            pass
        
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)

		# pass the blob through the network and obtain the detections and
        # predictions
        start = time.time()
        net.setInput(blob)
        detections = net.forward() # ->all object_detection happening here
        end = time.time()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                errorGuess = 0
                # extract the index of the class label from the
                # detections, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # collect info about the detected object
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

                ##########
                # CUSTOM FILTER
                ##########
                newObj = detectedObject(name, posInFrame, timestamp, location, confidence)
                timeDeltas = []
                posDeltas = []

                # Make sure the buffer isn't empty
                if not objectBuffer:
                    print("First object Detected")
                    logDetection(filePath, newObj)
                    objectBuffer.append(newObj)
                else:
                    # check all previous instances of this object
                    for oldObj in objectBuffer:
                        if oldObj.name == newObj.name:
                            # get last time this type was logged
                            timeDelta = (newObj.time - oldObj.time).total_seconds()
                            timeDeltas.append(timeDelta)

                            # get how much this object has moved on the screen
                            posDelta = newObj.pos[0] - oldObj.pos[0]
                            posDelta = abs(posDelta)
                            posDeltas.append(posDelta)

                            # info-vis.
                            text = "P-Delta of "+ newObj.name +" : "+ str(posDelta)
                            cv2.putText(frame, text, (5, 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                            text = "T-Delta of "+ newObj.name + " : " + str(timeDelta)
                            cv2.putText(frame, text, (5, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                    # decice if this is a new object or not
                    if not timeDeltas:
                        print("Nothing like this in the buffer")
                        logDetection(filePath, newObj)
                    elif min(timeDeltas) > 5 or min(posDeltas) > 100:
                        logDetection(filePath, newObj)

                    objectBuffer.append(newObj)
                    amout_of_individuals_detected += 1

                ##########
                # REIDENTIFICATION
                ##########

        # keep buffer small
        if len(objectBuffer) > 25:
            del(objectBuffer[0:5])

        if errorGuess > 600:
            warn = "No new object for a while, mayber there's an Error!"
            col = (50, 0, 240)
            cv2.putText(frame, warn, (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, col, 2)

        # CREATE OUTPUT VIDEO
        # check if the video writer is None
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter("videos/output.avi", fourcc, 30,
                (frame.shape[1], frame.shape[0]), True)
            # some information on processing single frame
            if total > 0:
                elap = (end - start)
                print("[INFO] single frame took {:.4f} seconds".format(elap))
                print("[INFO] estimated total time to finish: {:.4f}".format(
                    elap * total))
        # write the output frame to disk
        writer.write(frame)


        # show the output frame with all added INFO,
        # or create a new window if destroyed
        if output_flag.value == True:
            cv2.imshow("Object Detection Running", frame)
        key = cv2.waitKey(1) & 0xFF


    # dump FPS info
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup when the thread runs out
    objectBuffer.clear()
    cv2.destroyAllWindows()
    vs.stop()
    writer.release()
