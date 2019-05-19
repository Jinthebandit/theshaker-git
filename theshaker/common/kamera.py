#! /Projects/camera.py python3

import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from skimage.measure import compare_ssim

class camera:
	def calibrate(self,msg):
		camera = PiCamera()
		camera.resolution = (640,480)

		rawCapture1 = PiRGBArray(camera)
		time.sleep(0.5)

		camera.capture(rawCapture1, format="bgr")
		calibrate = rawCapture1.array

		cv2.imwrite("../Pictures/calibrate.jpg", calibrate)
		camera.close()

	def compare(self,msg):
		camera = PiCamera()
		camera.resolution = (640,480)

		rawCapture2 = PiRGBArray(camera)
		time.sleep(0.5)

		camera.capture(rawCapture2, format="bgr")
		compare = rawCapture2.array

		calibrate = cv2.imread("../Pictures/calibrate.jpg")

		roiA = calibrate[130:460, 140:600]
		roiB = compare[130:460, 140:600]

		grayA = cv2.cvtColor(roiA, cv2.COLOR_BGR2GRAY)
#		grayA = cv2.GaussianBlur(grayA, (5,5), 0)

		grayB = cv2.cvtColor(roiB, cv2.COLOR_BGR2GRAY)
#		grayB = cv2.GaussianBlur(grayB, (5,5), 0)

		(score, diff) = compare_ssim(grayA, grayB, full=True)
		diff = (diff * 255).astype("uint8")

		cv2.imwrite("../Pictures/difference.jpg", diff)

		camera.close()

		percent = 100*score
		if score >= 0.6:
			print("Uebereinstimmung: " + str(percent) + "Prozent")
			print("mehr steine")
		else:
			print("Form ist voll: Programm beenden")

#camera.calibrate(" "," ")
#time.sleep(1)
#camera.compare(" "," ")
