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
    def __init__(self):
        pass

    # Take a picture with the camera and save it
    def calibrate(self, msg):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.rotation = 90

        raw_capture1 = PiRGBArray(camera)
        time.sleep(0.5)

        camera.capture(raw_capture1, format='bgr')
        calibrate = raw_capture1.array

        cv2.imwrite('/home/pi/Pictures/calibrate.jpg', calibrate)
        camera.close()

    # Load the calibration picture and compare it with a new picture
    def compare(self, msg):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.rotation = 90
        raw_capture2 = PiRGBArray(camera)
        time.sleep(0.5)
        camera.capture(raw_capture2, format='bgr')
        compare = raw_capture2.array
        cv2.imwrite('/home/pi/Pictures/compare.jpg', compare)
        time.sleep(0.1)

        calibrate = cv2.imread('/home/pi/Pictures/calibrate.jpg')
        compare = cv2.imread('/home/pi/Pictures/compare.jpg')

        # Region of Interest [y1:y2, x1:x2]
        roi_a = calibrate[100:370, 70:550]
        roi_b = compare[100:370, 70:550]

        # Color correction
        gray_a = cv2.cvtColor(roi_a, cv2.COLOR_BGR2GRAY)
        gray_a = cv2.GaussianBlur(gray_a, (5,5), 0)
        gray_b = cv2.cvtColor(roi_b, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.GaussianBlur(gray_b, (5,5), 0)

        # Compare the images, return difference and score (score of 1 = no difference)
        (score, diff) = compare_ssim(gray_a, gray_b, full=True)
        diff = (diff * 255).astype('uint8')

        # Save difference image and compare image
        cv2.imwrite('/home/pi/Pictures/difference.jpg', diff)
        cv2.imwrite('/home/pi/Pictures/compare.jpg', gray_b)
        camera.close()

        # Send MQTT message containing the difference in percent and the load status of the form
        percent = round((score-0.35) * 156)
        if percent > 100:
            percent = 100
        if percent < 0:
            percent = 0
        load = 100 - int(percent)
        client = mqtt.Client('')
        client.connect(config.BROKER, config.PORT, 60)
        client.publish('pdp/score', score)
        time.sleep(0.1)
        client.publish('pdp/load', load)

        return load
