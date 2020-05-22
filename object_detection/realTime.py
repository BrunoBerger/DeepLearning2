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
		configPath = os.path.sep.join([args["type"], args["model"],  configFile ])
		weightsPath = os.path.sep.join([args["type"], args["model"], weightsFile ])
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

####################################
####################################
####################################
####################################
def mnSSD_Detection(args, run_flag):
	###MNSSD TYPE
	##################
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
	fps = FPS().start()

	f = open("../object_log.csv", "w+")
	f.close()

	# loop over the frames from the video stream
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

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > args["confidence"]:
				# extract the index of the class label from the
				# `detections`, then compute the (x, y)-coordinates of
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

				position = gps.givePosition()
				with open('../object_log.csv','a') as file_:
					file_.write("{},{},{},{},{}".format(label,
						"%.2f" % confidence,
						position[0], position[1],
						datetime.now()))
					file_.write("\n")

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

########################################
########################################
########################################
########################################
def yolo_Detection(args, run_flag):
	###YOLO TYPE

	#start getting the video form webcam 0
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	fps = FPS().start()

	#create resizeable window
	# cv2.namedWindow('betterWindow', flags= cv2.WINDOW_GUI_NORMAL)

	# Reset csv-Data
	f = open("../object_log.csv", "w+")
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

		# determine only the *output* layer names that we need from YOLO
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

		# construct a blob from the input image and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes and
		# associated probabilities
		blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), ##TODO
			swapRB=True, crop=False)
		net.setInput(blob)

		start = time.time()
		layerOutputs = net.forward(ln)
		end = time.time()

		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > args["confidence"]:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

		# apply non-maxima suppression to suppress weak, overlapping bounding
		# boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
			args["threshold"])

		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				# draw a bounding box rectangle and label on the image
				color = [int(c) for c in COLORS[classIDs[i]]]
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
				cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
					0.5, color, 2)


		# output the names of detected objets
		for x in range(len(idxs)):
		    print(LABELS[classIDs[x]],
				" detected, with ", "%.2f" % confidences[x],
				 " confidence in {:.6f} seconds".format(end - start))

		for x in range(len(idxs)):
			position = gps.givePosition()
			with open('../object_log.csv','a') as file_:
				file_.write("{},{},{},{},{}".format(
					LABELS[classIDs[x]],
					"%.2f" % confidences[x],
					position[0], position[1],
					datetime.now()))
				file_.write("\n")

		# show the output frame
		cv2.imshow("wayCoolerWindow", frame)
		# if the `q` key was pressed, break from the loop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
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
	if args["type"] == "MobileNetSSD":
		mnSSD_Detection(args, run_flag)

	elif args["type"] == "yolo-coco":
		yolo_Detection(args, run_flag)

	else:
		print("[ERROR] Select a detection-type")
		exit()
