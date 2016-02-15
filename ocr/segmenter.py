import blobdetection
import cropmarkup
import cropsection

import cv2
def getImages(imagePath):
    """
    Args:
        filename: the path to the imge file to segment

    Returns:
        Returns the sections filenames that are the results.
    """

    # Cut out the markup area
    sidePath = cropmarkup.getMarkupTab(imagePath)

    if (sidePath == None):
        raise Exception("Can't do it")

