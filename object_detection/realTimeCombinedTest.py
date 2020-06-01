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
def setup(args):
	# for shorter file-paths
	os.chdir("object_detection")

	print("Chosen Model Type:", args["type"])

	global net
	global COLORS

	# Load a yolo model
	if args["type"] == "yolo-coco":
		#get the names of the cfg and weights files for the chosen model
		for file in os.listdir(os.path.sep.join([args["type"], args["model"]])):
			if file.endswith(".cfg"):
				configFile = file
			if file.endswith(".weights"):
				weightsFile = file

		# assign the paths to the files based on the arguments
		configPath = os.path.sep.join([args["type"], args["model"], configFile])
		weightsPath = os.path.sep.join([args["type"], args["model"], weightsFile])
		labelsPath = os.path.sep.join([args["type"], "coco.names"])
		global LABELS
		LABELS = open(labelsPath).read().strip().split("\n")

		# initialize a list of colors to represent each possible class label
		np.random.seed(42)
		COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
			dtype="uint8")

		print("[INFO] Setup, done, loading the ", args["model"], "model")
		net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	elif args["type"] == "SSD-Mobilenet-v2":
		print("This may come later")
		exit()

	elif args["type"] == "MobileNetSSD":
		global CLASSES

		CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
			"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
			"sofa", "train", "tvmonitor"]
		COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

		net = cv2.dnn.readNetFromCaffe("MobileNetSSD/MobileNetSSD_deploy.prototxt.txt",
			"MobileNetSSD/MobileNetSSD_deploy.caffemodel")

	else:
		print("[ERROR]:Specify a '--type' ")
		exit()


def detection(args, run_flag):

	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
	fps = FPS().start()

	# Reset csv-Data
	f = open("../logs/object_log.csv", "w+")
	f.close()

	#output the Video Stream
	while run_flag.value:
		#grab frame and its dimensions
		# frame = vs.read()
		try:
			frame = vs.read()
			(H, W) = frame.shape[:2]
		except AttributeError:
			print ("[ERROR] Please connect a Webcam to the PC")
			exit()



		# construct a blob from the input image ..
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (256, 256)),
			0.007843, (256, 256), 127.5)

		# determine only the *output* layer names that we need from YOLO
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

		# ... and then perform a forward pass of the object detector,
		# giving us our bounding boxes and associated probabilities
		# + measure the time for performance-info
		start = time.time()
		net.setInput(blob)

		if args["type"] == "MobileNetSSD":
			detections = net.forward()
		elif args["type"] == "yolo-coco":
			detections = net.forward()
		# detections = net.forward(ln)

		end = time.time()

		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > args["confidence"]:

				# extract the index of the class label from the
				# `detections`, then compute the (x, y)-coordinates of
				# the bounding box for the object
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
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
				print(label," detected in {:.6f} seconds".format(end - start))

		# show the output frame
		cv2.imshow("wayCoolerWindow", frame)
		# if the `q` key was pressed, break from the loop
		key = cv2.waitKey(1) & 0xFF
		# if key == ord("q"):
		# 	break


	# update the FPS counter
	fps.update()
	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()






def main(args, run_flag):
	setup(args)
	detection(args, run_flag)
	print("[INFO] Exiting detection")
