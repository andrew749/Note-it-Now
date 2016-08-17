import cv2
import numpy as np

"""
This class is used to find the keypoints on an image and return them.
"""

"""
A type for shapes
"""
class Shapes:
    TRIANGLE, SQUARE, CUSTOM = range(3, 6)

"""
Class for a shape.
"""
class Shape:
    type = None
    origin = None
    def __init__(self, origin, type):
        self.type = type
        self.origin = origin
    def __str__(self):
        return self.type

"""
Helper to get the type of shape given an enumeration and the number of sides
"""
def getShapeType(numberSides):
    if (len(numberSides) == 3):
        return Shapes.TRIANGLE
    elif (len(numberSides) == 4):
        return Shapes.SQUARE
    else:
        return Shapes.CUSTOM

def findShapes(tempimage):
    grayscale = cv2.cvtColor(tempimage, cv2.COLOR_BGR2GRAY)
    _, grayscale = cv2.threshold(grayscale, 60, 255, cv2.THRESH_TOZERO)

    # intermediate grayscale file to prevent keeping too much data in RAM
    cv2.imwrite('test.jpg', grayscale)
    shapeMask = cv2.inRange(grayscale, 0, 60)
    (cnts, _) =  cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapeArray = []
    for c in cnts:
        #approximate the shape
        result = cv2.approxPolyDP(curve=c, epsilon=cv2.arcLength(c, True) * 0.01, closed=True)

        #find Moments for center calculation
        M = cv2.moments(result)

        # Check to see if the contour matches
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            type = getShapeType(result)
            print type
            if type is not None:
                shapeArray.append(Shape((cx,cy),type))

    # Helper to take the keypoints and generate images with the points highlighted
    def generate_and_draw_keypoints(image, data):
        keypoints = [cv2.KeyPoint(x.origin[0], x.origin[1], 10) for x in data ]
        kp = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite('imageayy.jpg', kp)

    generate_and_draw_keypoints(tempimage, shapeArray)

    # array of shapes storing location of interesting points on an image.
    return shapeArray

def getShapes(image):
    return findShapes(image)
