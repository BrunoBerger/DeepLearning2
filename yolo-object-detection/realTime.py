#https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2


vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()



cv2.namedWindow('betterWindow', flags= cv2.WINDOW_GUI_NORMAL)

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

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
