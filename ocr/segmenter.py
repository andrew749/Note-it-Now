import blobdetection
import cropmarkup
import cropsection
import math
import cv2

import uuid

def getImages(imagePath):
    """
    Args:
        filename: the path to the imge file to segment

    Returns:
        Returns the sections filenames that are the results.
    """
    # Read in the image
    im = cv2.imread(imagePath, cv2.IMREAD_COLOR)

    height, width = im.shape[:2]

    print(im[5,:,2])

    # Requires that red is present to find appropriate point
    markupImage = cropmarkup.getMarkupTab(im)

    if (markupImage is None):
        raise Exception("Can't find a margin.")

    cv2.imwrite('Image.jpg', markupImage)

    # Find all of the markup points in the image
    shapes = blobdetection.getShapes(markupImage)

    if (shapes == None or len(shapes) == 0 ):
        raise Exception("Can't find any shapes.")

    # Sort them by the ones closest to the top
    shapes.sort(key=lambda x: x.origin[1])
    imageArray = []

    print ("before")
    print shapes
    merge_close_neighbors(shapes)
    print ("after")
    print (shapes)


    # For each landmark, cut a section from either the top of the page or from landmark to landmark
    for x in range(0, len(shapes)):
        tempImage = None
        if (x + 1 >= len(shapes)):
            tempImage = cropsection.getSection(im, shapes[x].origin, (width, height))
        else:
            tempImage = cropsection.getSection(im,shapes[x].origin, (width, shapes[x+1].origin[1]))
        tempPath = "static/temp/{}.jpg".format(uuid.uuid4())
        imageArray.append(tempPath)
        cv2.imwrite(tempPath, tempImage)
    return imageArray

def merge_close_neighbors(data):
    i = 0
    while i < len(data) - 1:
        while i + 1 < len(data) and  abs(data[i+1].origin[1] - data[i].origin[1]) < 20:
            del (data[i+1])
        i += 1
