import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt

def showImage(image, name="Test image"):
    cv2.imshow(name, image)
    cv2.waitKey()

def removeBackgroundLines(image):
    """
    remove the blue lines
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
    #load in the image
    cleanedImage = removeBackgroundLines(image)
    """
    Get a better bounding box so we can cut out text
    """
    # rgb_masked_image = cv2.cvtColor(res, cv2.COLOR_HSV2RGB)
    # gray_masked_image = cv2.cvtColor(rgb_masked_image, cv2.COLOR_RGB2GRAY)

    #kernel for image operations on a long block of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))

    # Filter out some noise
    closing = cv2.morphologyEx(cleanedImage, cv2.MORPH_CLOSE, kernel)

    showImage(closing)
    closing_rgb = cv2.cvtColor(closing,  cv2.COLOR_HSV2RGB)
    closing_gray = cv2.cvtColor(closing_rgb, cv2.COLOR_RGB2GRAY)

    showImage(closing_gray)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
    filter_noise = cv2.morphologyEx(closing_gray, cv2.MORPH_OPEN, vertical_kernel)
    showImage(filter_noise)


    # one_more_filter = cv2.morphologyEx(filter_noise, cv2.MORPH_CLOSE, kernel)
    one_more_filter = cv2.blur(filter_noise, (40,5))
    # showImage(one_more_filter)

    contours, _ = cv2.findContours(one_more_filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    im_example = img.copy()
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(im_example, (x,y), (x+w, y+h), (0,0, 255), 2)

    showImage(im_example)

