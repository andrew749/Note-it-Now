import cv2
import numpy as np
import math
import pdb
import uuid

"""
This class is used to find the keypoints on an image and return them.
"""
#A type for shapes
class Shapes:
    TRIANGLE, SQUARE, PENTAGON, HEXAGON = range(3, 7)

class Shape:
    type = None
    origin = None
    def __init__(self, origin, type):
        self.type = type
        self.origin = origin
    def __str__(self):
        return self.type


def getShapeType(numberSides):
    print len(numberSides)
    if (len(numberSides) == 3):
        return Shapes.TRIANGLE
    elif (len(numberSides) == 4):
        return Shapes.SQUARE
    elif (len(numberSides) == 5):
        return Shapes.PENTAGON
    elif (len(numberSides) == 6):
        return Shapes.HEXAGON
    else:
        return None

def findShapes(image):
    lower = np.array([0], dtype=np.uint8)
    upper = np.array([15], dtype=np.uint8)
    shapeMask = cv2.inRange(image, lower, upper)
    (cnts, _) =  cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapeArray = []
    for c in cnts:
        #approximate the shape
        result = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
        #find moments for center calculation
        M = cv2.moments(result)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            shapeArray.append(Shape((cx,cy), getShapeType(result)))
    return shapeArray

def getShapes(image):
    return findShapes(image)
