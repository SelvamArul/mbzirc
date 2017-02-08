'''
This file creates synthetic training data Haar cascade classifier.
Idea:
Use the positive annotations.
open the each image in the positive annotations and its corresponding yaml file
crop out patches from the image other than the positive annotation
'''
import sys
import cv2
import os
import yaml
import glob

if len(sys.argv) != 3:
	print('usage synthesize_negative_samples.py positive_samples_dir output_dir')
	sys.exit(0)

POS_DIR = sys.argv[1]
OUT_DIR = sys.argv[2]
FILE_NAMES = {}
CROP_HEIGHT = 200
CROP_WIDTH = 200

'''
Load file names in the POS_DIR
'''
def load_file_names():
	global  FILE_NAMES
	FILE_NAMES = glob.glob(POS_DIR + '/fr*.jpg')

'''
Load the points for positive annotation from the yaml file
Load only 1st and 3rd point -Enough for defining a rectangle
'''
def load_points(filename):
	p1 = p3 = 0
	with open(filename, 'r') as stream:
		yaml_data = yaml.load(stream)
		p1 = yaml_data['polygons'][0]['points'][0]
		p3 = yaml_data['polygons'][0]['points'][2]
	return p1, p3

def crop_negative_samples(filename, p1, p3):
	print (filename, p1, p3)
	img = cv2.imread(filename, 0)
	prefix = ii.split('/')[-2]
	rgb_name = ii.split('/')[-1]

	img_rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
	# cv2.circle(img_rgb, tuple(p1), 5, (0, 0, 255), thickness=5)
	# cv2.circle(img_rgb, tuple(p3), 5, (0, 255, 0), thickness=5)
	# cv2.imshow('img', img_rgb)
	# cv2.waitKey(0)

	# p1 is the third point
	# p3 is the first point
	count = 0
	for i in range(0, img.shape[1] - 2 * CROP_HEIGHT, CROP_HEIGHT):
		for j in range(0, img.shape[0] - 2 * CROP_WIDTH, CROP_WIDTH):
			if (i >= p3[0] and j >= p3[1] and i <= p1[0] and j <= p1[1]) or \
					(i+CROP_HEIGHT >= p3[0] and j+CROP_WIDTH >= p3[1] and i+CROP_HEIGHT <= p1[0] and j+CROP_WIDTH <= p1[1]):
				print (p3, p1, i, j)
				# cv2.circle(img_rgb, tuple([i,j]), 5, (0, 0, 255), thickness=5)
				# cv2.circle(img_rgb, tuple([i+CROP_HEIGHT, j+CROP_WIDTH]), 5, (0, 255, 0), thickness=5)
				# cv2.imshow('img', img_rgb)
				# cv2.waitKey(0)
				# sys.exit(0)
				print ('continue ------------------------------->')
				continue
			if count == 25:
				img_rgb[ j:j + CROP_WIDTH, i: i + CROP_HEIGHT] = (255, 0, 0)
				cv2.circle(img_rgb, tuple(p3), 10, (0, 0, 255), thickness=10)
				cv2.circle(img_rgb, tuple(p1), 10, (0, 255, 0), thickness=10)
				cv2.circle(img_rgb, tuple([i,j]), 5, (0, 0, 255), thickness=5)
				cv2.circle(img_rgb, tuple([i+CROP_HEIGHT, j+CROP_WIDTH]), 5, (0, 255, 0), thickness=5)
				cv2.imshow(rgb_name, img_rgb)
				cv2.waitKey(0)
				# sys.exit(0)
			crop = img [j:j+CROP_WIDTH, i: i+CROP_HEIGHT]
			cv2.imwrite(OUT_DIR + '/{}_{}_crop{}.png'.format(prefix,rgb_name,count), crop)
			count += 1
			#cv2.waitKey(0)
	print ('Done ', rgb_name)
if __name__ == '__main__':
	load_file_names()
	print (FILE_NAMES)
	for ii in FILE_NAMES:
		rgb_name = ii.split('/')[-1]
		yaml_name = '/'.join(ii.split('/')[0:-1]) + '/'+ rgb_name.split('.')[0] + '.yaml'
		print ('yaml_name', yaml_name)
		p1, p3 = load_points(yaml_name)
		crop_negative_samples(ii, p1, p3)

	print ('Done all')
