#! /common/kamera.py python3

# Library Imports
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from skimage.measure import compare_ssim
import paho.mqtt.client as mqtt

# Local Imports
from ..data.settings import config

class kamera:
	# Erstellt Foto zur Kalibrierung und speichert es zur spaeteren Verwendung
	def calibrate(self,msg):
		camera = PiCamera()
		camera.resolution = (640,480)
		camera.rotation = 90

		rawCapture1 = PiRGBArray(camera)
		time.sleep(0.5)

		camera.capture(rawCapture1, format="bgr")
		calibrate = rawCapture1.array

		cv2.imwrite("/home/pi/Pictures/calibrate.jpg", calibrate)
		camera.close()

	# Ladet das Kalibrierungsfoto und vergleicht es mit einer neuen Aufnahme
	def compare(self,msg):
		camera = PiCamera()
		camera.resolution = (640,480)
		camera.rotation = 90
		rawCapture2 = PiRGBArray(camera)
		time.sleep(0.5)
		camera.capture(rawCapture2, format="bgr")
		compare = rawCapture2.array
		cv2.imwrite("/home/pi/Pictures/compare.jpg", compare)
		time.sleep(0.1)

		calibrate = cv2.imread("/home/pi/Pictures/calibrate.jpg", mode="RGB")
		compare = cv2.imread("/home/pi/Pictures/compare.jpg", mode="RGB")
	
		# Beschraenkt die area of interest auf die Form. Region of Interest [y1:y2, x1:x2]
		roiA = calibrate[110:360, 100:550]
		roiB = compare[110:360, 100:550]

		# Farbanpassung beider Aufnahmen
		grayA = cv2.cvtColor(roiA, cv2.COLOR_BGR2GRAY)
		grayA = cv2.GaussianBlur(grayA, (5,5), 0)
		grayB = cv2.cvtColor(roiB, cv2.COLOR_BGR2GRAY)
		grayB = cv2.GaussianBlur(grayB, (5,5), 0)

		# Vergleich der Aufnahmen und Ausgabe der Veraenderung in Grautoenen
		(score, diff) = compare_ssim(calibrate, compare, full=True)
		diff = (diff * 255).astype("uint8")
	
		# Vergleichsbild speichern und Kamera schliessen
		cv2.imwrite("/home/pi/Pictures/difference.jpg", diff)
		camera.close()
		
		# MQTT Nachricht mit Score in Prozent und Fuellstand senden
		percent = round(score*100)
		load = 100-int(percent)
		client = mqtt.Client("")
		client.connect(config.BROKER,config.PORT,60)
		client.publish("pdp/score",percent)
		time.sleep(0.1)
		client.publish("pdp/load",load)

		return score
