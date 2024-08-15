import cv2
import platform

def capture():
	if platform.system() != 'Linux':
		image = cv2.imread('test_images/01.jpg')
	else:
		# TODO: read image from raspberry pi camrea
		pass
	return image

def get_progress(image):
	# TODO: extract progress from display
	error = None
	progress = 23
	return error, progress