import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt

def showImage(image, name="Test image"):
    """
    Helper to show an image given a path
    Used for debugging.
    """
    cv2.imshow(name, image)
    cv2.waitKey()

def removeBackgroundLines(image):
    """
    Remove the blue lines from a sheet of paper
    """
    # load the image and hue and saturation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110,50,50])
    upper_blue = np.array([140,90,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

     # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)

    return res


def getSentences(image):
    """
    Find the sentences in an image and return the rects for each one
    """
    #load in the image
    cleanedImage = removeBackgroundLines(image)
    rgb_masked_image = cv2.cvtColor(cleanedImage, cv2.COLOR_HSV2RGB)
    gray_masked_image = cv2.cvtColor(rgb_masked_image, cv2.COLOR_RGB2GRAY)

    #kernel for image operations on a long block of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))

    # Filter out some noise
    closing = cv2.morphologyEx(cleanedImage, cv2.MORPH_CLOSE, kernel)

    # showImage(closing)
    closing_rgb = cv2.cvtColor(closing,  cv2.COLOR_HSV2RGB)
    closing_gray = cv2.cvtColor(closing_rgb, cv2.COLOR_RGB2GRAY)

    # showImage(closing_gray)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
    filter_noise = cv2.morphologyEx(closing_gray, cv2.MORPH_OPEN, vertical_kernel)
    # showImage(filter_noise)

    one_more_filter = cv2.blur(filter_noise, (40,5))

    contours, _ = cv2.findContours(one_more_filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    im_example = image.copy()
    bounding_rects = []
    for contour in contours:
        tempRect = cv2.boundingRect(contour)
        bounding_rects.append(tempRect)
        x,y,w,h = tempRect
        cv2.rectangle(im_example, (x,y), (x+w, y+h), (0,0, 255), 2)
        cv2.imwrite('sliceslice.jpg', gray_masked_image[y:y+h, x:x+w])

    # showImage(im_example)
    return bounding_rects

image = cv2.imread('slice.jpg')
getSentences(image)
