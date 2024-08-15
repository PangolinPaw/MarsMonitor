import cv2
import numpy as np
import platform

def capture():
    '''Capture still image from camera'''
    if platform.system() != 'Linux':
        image = cv2.imread('test_images/01.jpg')
    else:
        # TODO: read image from raspberry pi camrea
        pass
    image = resize(image, 800)
    return image

def find_circle(image):
    '''Find the circles that surround the progess % to narrow down text recognition target area'''
    image_copy = image.copy()
    gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (3,3))
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        20,
        param1=10,
        param2=50,
        minRadius=100,
        maxRadius=150
    )
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            print(radius)
            cv2.circle(
                image,
                center,
                radius,
                (  0,  0, 255),
                2
            )
    return image

def get_progress(image):
    '''Find and parse progress % from UI'''
    error = None
    progress = 23
    masked_image = mask_display(image)
    circled_image = find_circle(masked_image)
    cv2.imshow('image', circled_image)
    cv2.waitKey(0)
    return error, progress

def mask_display(image):
    '''Exclude eveything from the image except white elements to reduce noise'''
    white = {
        'min':(  0,   0, 230),
        'max':(179,   6, 255)
    }
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, white['min'], white['max'])
    masked = cv2.bitwise_and(image, image, mask=mask)
    return masked

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    '''Resize image to more manageable dimensions for faster processing'''
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized