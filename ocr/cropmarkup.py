import cv2
import numpy as np
"""
beginning and end are keypoints and imagePath is the name/path of the image
For easy processing of sidebar
"""
def getMarkupTab(image):
    #fallback margin size approximation so we can exit
    left = 0
    top  = 0

    width, height = image.shape[:2]

    bottom = height

    print "{width} x {height}".format(width=width, height=height)

    #scan left to right and try to find the red value
    smallestmargin = 0
    for x in range(0, width):
        for y in range(0, height):

            # Check individual pixel values
            pixel = image[y,x]

            b = pixel[0]
            g = pixel[1]
            r = pixel[2]

            temp_gb = np.uint16(g)+np.uint16(b)
            if r > 230 and temp_gb < 320:
                smallestmargin = x
                # check for a high red value
                return image[top:bottom, left:x]

    return None



