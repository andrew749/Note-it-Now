import cv2
import numpy as np

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

def findShapes(tempimage):
    grayscale = cv2.cvtColor(tempimage, cv2.COLOR_BGR2GRAY)
    shapeMask = cv2.inRange(grayscale, 0, 30)
    (cnts, _) =  cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapeArray = []
    for c in cnts:
        #approximate the shape
        result = cv2.approxPolyDP(c, 1, True)
        #find moments for center calculation
        M = cv2.moments(result)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            type = getShapeType(result)
            if type is not None:
                shapeArray.append(Shape((cx,cy),type))
    def generateAndDrawKeypoints(image, data):
        keypoints = [cv2.KeyPoint(x.origin[0], x.origin[1], 10) for x in data ]
        kp = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite('imageayy.jpg', kp)

    generateAndDrawKeypoints(tempimage, shapeArray)
    return shapeArray
def getShapes(image):
    return findShapes(image)
