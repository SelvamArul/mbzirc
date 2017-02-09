import sys
import cv2
import os
import numpy as np

num_imgs = [21, 18, 45, 4, 95, 56, 9]

pos = '/home/arul/mbzirc/wrench_perception/data/positives/'
neg = '/home/arul/mbzirc/wrench_perception/data/negatives/3_frame0013.jpg'

cascade = cv2.CascadeClassifier('/home/arul/mbzirc/wrench_perception/data/haar_data/outputWrench/cascade_16.xml')

minlen = int(1200 / 15.)
maxlen = int(1200 / 1.5)

def validate_cascade():
	for i in range(1, 8, 1):
		for jj in range(1, num_imgs[i-1], 3):
			img_name = '{}{}/frame{:04d}.jpg'.format(pos, i, jj)
			print (img_name)
			img = cv2.imread(img_name, 0)
			img = cv2.resize(img, (img.shape[1] / 2, img.shape[0] / 2))
			# cv2.imshow('test_image', img)
			# cv2.waitKey(0)
			imgrgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

			result = cascade.detectMultiScale(img, scaleFactor=1.35, minNeighbors=3)
			# minSize=(minlen, minlen), maxSize=(maxlen, maxlen)
			if type(result) != 'tuple':
				for (x, y, w, h) in result:
					cv2.rectangle(imgrgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.imwrite('resource/predictions/{}_frame_{:04d}.jpg'.format(i, jj), imgrgb)
			else:
				print ('No Predictions for ', img_name)

'''
idea: crop the image to retain only the part of image lower than the bounding box
	build image pyramid and do template matching
'''

def locate_wrenches(img_name):
	img = cv2.imread(img_name, 0)
	img = cv2.resize(img, (img.shape[1] / 2, img.shape[0] / 2))
	# cv2.imshow('test_image', img)
	# cv2.waitKey(0)
	imgrgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

	results = cascade.detectMultiScale(img, scaleFactor=1.35, minNeighbors=2)
	if type(results) != 'tuple':
		result = sorted(results, key=lambda results: results[2] * results[3])
		print ('results')
		# for ii in results:
		# 	print ii
		result = result[-1].reshape((1, 4))
		# print (result)
		# print (type(result))
		# print (result.shape)
		for (x, y, w, h) in result:
			cv2.rectangle(imgrgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.imshow('pred', imgrgb)
			cv2.waitKey(0)
			cropped = imgrgb[y:, :]
			cv2.imshow('cropped', cropped)
			cv2.waitKey(0)

		sys.exit(0)
	else:
		print ('No Predictions for ', img_name)

if __name__ == '__main__':
	#validate_cascade()
	locate_wrenches('/home/arul/mbzirc/wrench_perception/data/positives/1/frame0003.jpg')

