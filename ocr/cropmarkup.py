from PIL import Image
import uuid
"""
beginning and end are keypoints and imagePath is the name/path of the image
For easy processing of sidebar
"""
def getMarkupTab(imagePath):
    #fallback margin size approximation so we can exit
    marginSize = None

    original = Image.open(imagePath)
    width,height = original.size

    #initial scanning parameters
    left = 0
    top = 5

    rgb  =  original.convert('RGB')

    # restrict scanning to a third of a page
    for x in range(0,width/3):
        # Check individual pixel values
        r,g,b = rgb.getpixel((x,0))
        # print ("red:{red} green:{green} blue:{blue}".format(red=r,green=g,blue=b))
        if (g + b < 400):
            #check for a high red value
            marginSize = x

    # Want to escape if we couldn't find a margin.
    if marginSize is None:
        return None

    print marginSize
    right = marginSize

    #cut out the entire margin
    bottom = height

    # Crop the image for later processing
    cropped_example = original.crop((left,
                                     top,
                                     right,
                                     bottom
                                     ))
    tempFileName = "static/temp/"+str(uuid.uuid4()) +".jpg"
    cropped_example.save(tempFileName)

    # Test code to show the cropped image
    cropped_example.show()
    return tempFileName
