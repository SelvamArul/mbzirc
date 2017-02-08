import cv2
from matplotlib import pyplot as plt
import sys
import numpy as np

def show_image(window_name, img):
	cv2.imshow(window_name, img)
	cv2.waitKey(0)


def computeMinMax_in_X(img):
	min = img.shape[1]
	max = 0
	print ('min max', np.amin(img), np.amax(img) )
	print ('unique', np.unique(img))
	for i in range(0,img.shape[1]):
		oneRow = img[:,i]
		if np.any(oneRow == 255) == True:
			if i < min:
				min = i
			if i > max:
				max = i
	print ('min max X', min, max)
	sys.exit(0)



def main():
	input_img = cv2.imread('resource/frame0000.jpg', 0)
	img = input_img.copy()
	imgrgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
	print ('imgrgb shape', imgrgb.shape)
	template = cv2.imread('resource/wrench_big_1.png', 0)
	#show_image('template', template)
	print(template.shape)

	template_shape = template.shape
	edges = cv2.Canny(img, 100, 200)
	edgesrgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
	print ('edges', edgesrgb.shape)

	res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)

	# Algo:
	# Assumptions:
	#   1. The image has all the five wrenches
	#   2. Template matching finds all the wrenches
	# steps:
	#   begin
	#       get min, max location in the res image and min location is the point of interest
	#       highlight the rectangular area(size of the template) around the min point in the input image
	#       This area has the wrench in it
	#       clear the rectangular area around the min location in res image.
	#       This enables the detection of the next wrench
	#       if not all the wrenches are detected, go to begin

	count = 0
	while count < 5 :

		minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
		minLoc_ = (minLoc[0] + template_shape[1]/2,  minLoc[1] + template_shape[0] / 2)

		# paint the image to highlight the wrench
		cv2.circle(imgrgb, minLoc_, 10, (255,0,0), thickness = 10)
		p1 = (minLoc_[0] - template.shape[1]/2, minLoc_[1] - template.shape[0]/2)
		p2 = (minLoc_[0] + template.shape[1]/2, minLoc_[1] + template.shape[0]/2)

		cv2.rectangle(imgrgb, p1, p2, (255,count*50,0), thickness=5)

		print ('res ', res.shape)
		edges_crop  = edges[p1[1]:p1[1]+template_shape[0], p1[0]:p1[0]+template_shape[1] ]

		# show_image('res', res)
		plt.subplot(131), plt.imshow(res, cmap='gray')
		plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
		plt.subplot(132), plt.imshow(imgrgb, cmap='gray')
		plt.title('img'), plt.xticks([]), plt.yticks([])
		plt.subplot(133), plt.imshow(edgesrgb, cmap='gray')
		plt.title('edges'), plt.xticks([]), plt.yticks([])
		# plt.subplot(224), plt.imshow(edges_crop, cmap='gray')
		# plt.title('edges_crop'), plt.xticks([]), plt.yticks([])

		plt.suptitle('Template matching')
		plt.show()

		#computeMinMax_in_X(edges_crop)

		# clear out the rectangle boundary around the current wrench
		p3 = (minLoc[0] - template.shape[1] / 8, minLoc[1] - template.shape[0] / 2)
		p4 = (minLoc[0] + template.shape[1] / 8, minLoc[1] + template.shape[0] / 2)
		cv2.rectangle(res, p3, p4, (255, 255, 255), thickness=-1)
		count += 1

if __name__ == '__main__':
	main()