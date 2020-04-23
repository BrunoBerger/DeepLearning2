#Tis a mix of
#https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/
#and
#https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/
# run this script in its directory or adjust the yolo base path
#EXECUTE WITH:
# python yolo.py <--yolo yolo-coco> <--model <Tiny>/<320>>

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import argparse
import time
import cv2
import os

### SETUP
# construct the parser + arguments
#choose model between Tiny, 320, etc..
ap = argparse.ArgumentParser()
ap.add_argument("-y", "--yolo", required=False, default="yolo-coco",
	help="base path to YOLO directory")
ap.add_argument("-m", "--model", required=False, default="Tiny",
	help="chose between the yolov3 models 320 and Tiny")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

#get the names of the cfg and weights files for the chosen model
for file in os.listdir(os.path.sep.join([args["yolo"], args["model"]])):
	if file.endswith(".cfg"):
		configFile = file
	if file.endswith(".weights"):
		weightsFile = file

# assign the paths to the files based on the arguments
configPath = os.path.sep.join([args["yolo"], args["model"],  configFile ])
weightsPath = os.path.sep.join([args["yolo"], args["model"], weightsFile ])
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

print("[INFO] Setup, done, loading the ", args["model"], "model")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

###VIDEO

#start getting the video form webcam 0
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

#create resizeable window
cv2.namedWindow('betterWindow', flags= cv2.WINDOW_GUI_NORMAL)

#output the Video Stream
while True:
	#grab frame and its dimensions
	frame = vs.read()
	try:
		(H, W) = frame.shape[:2]
	except AttributeError:
		print ("[ERROR] Please connect a Webcam to the PC")

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

	# output the names of detected objets
	for x in range(len(idxs)):
	    print(LABELS[classIDs[x]],
			" detected, with ", "%.2f" % confidences[x],
			 " confidence in {:.6f} seconds".format(end - start))

	# show the output frame
	cv2.imshow("betterWindow", frame)
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
