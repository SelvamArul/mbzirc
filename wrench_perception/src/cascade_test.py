import sys
import cv2
import os
import numpy as np

pos = '/home/arul/mbzirc/wrench_perception/data/positives/1/frame0015.jpg'
neg = '/home/arul/mbzirc/wrench_perception/data/negatives/3_frame0013.jpg'


file = pos
if __name__ == '__main__':
	img = cv2.imread(file, 0)
	img = cv2.resize(img, (img.shape[1] / 2, img.shape[0] / 2))
	cv2.imshow('test_image', img)
	cv2.waitKey(0)
	imgrgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
	cascade = cv2.CascadeClassifier('/home/arul/mbzirc/wrench_perception/data/haar_data/outputWrench/cascade_13.xml')

	minlen = int(1200 / 15.)
	maxlen = int(1200 / 1.5)
	result = cascade.detectMultiScale(img, scaleFactor=1.35, minNeighbors=3)
	# minSize=(minlen, minlen), maxSize=(maxlen, maxlen)
	print (type(result))
	print (len(result))
	print result
	print (result.shape)
	index = 1
	for (x, y, w, h) in result:
		cv2.rectangle(imgrgb, (x, y), (x + w, y + h), (0, index * 30, 255), 2)
		cv2.imshow('Predictions', imgrgb)
		cv2.waitKey(0)
		index += 1
