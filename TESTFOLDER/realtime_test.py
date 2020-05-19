from imutils.video import VideoStream
import imutils
import cv2
import time

def OD(run_flag):
	print("Starting Webcam...")
	vs = VideoStream(src=0).start()
	time.sleep(1)

	while run_flag.value:

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

		frame = vs.read()
		try:
			frame = imutils.resize(frame, width=400)
		except AttributeError:
			print("[ERROR] Please connect a Webcam to the PC")
			exit()

		cv2.imshow("wayCoolerWindow", frame)

	cv2.destroyAllWindows()
	print("Stream Terminated")

def main():
	print("nothing")
