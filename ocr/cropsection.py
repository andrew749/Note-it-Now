from PIL import Image
import pdb
from cv2 import KeyPoint
import uuid
"""
beginning and end are keypoints and imagePath is the name/path of the image
"""
def getSection(beginning, end, imagePath):
    image = imagePath
    original = Image.open(image)
    left = 0
    top = beginning[1]
    right = end[0]
    bottom = end[1]
    cropped_example = original.crop((int(left),int(top), int(right), int(bottom)))
    tempFileName = "static/temp/"+str(uuid.uuid4())+ ".jpg"
    cropped_example.save(tempFileName)
    cropped_example.show()
    return tempFileName
