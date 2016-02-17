"""
beginning and end are keypoints and imagePath is the name/path of the image
"""
def getSection(image, beginning, end):
    left = int(beginning[0])
    top = 0 if beginning[1] < 30 else int(beginning[1]) - 30
    right = int(end[0])
    height = image.shape[0]
    bottom = height if height - end[1] < 30 else int(end[1]) + 30
    cropped_example = image[top:bottom, left:right]
    return cropped_example
