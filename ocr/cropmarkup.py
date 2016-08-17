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

    height, width = image.shape[:2]


    print "{width} x {height}".format(width=width, height=height)

    ## Iterate over the width then by height until we find a pixel red enough to make a decision
    for x in xrange(width):
        for y in xrange(height):

            # Check individual pixel values
            pixel = image[y,x]

            b, g, r = pixel

            temp_gb = np.uint16(g) + np.uint16(b)

            # Checking the green blue and red threshold values
            if r > 230 and temp_gb < 320:
                return image[ top : height, left : x]
    return None
