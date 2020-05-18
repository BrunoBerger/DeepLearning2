from imutils.video import VideoStream
import imutils
import cv2
import time

def initOD(run_flag):
	print("Starting Webcam...")
	vs = VideoStream(src=0).start()
	time.sleep(1)

	while run_flag.value:

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		cv2.imshow("wayCoolerWindow", frame)

	cv2.destroyAllWindows()
	print("Stream Terminated")

def main():
	print("nothing")
