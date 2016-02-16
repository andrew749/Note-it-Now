"""
beginning and end are keypoints and imagePath is the name/path of the image
"""
def getSection(image, beginning, end):
    left = int(beginning[0])
    top = int(beginning[1])
    right = int(end[0])
    bottom = int(end[1])
    cropped_example = image[top:bottom, left:right]
    return cropped_example
