import pytesseract
from PIL import Image
from PIL import ImageFilter
image = Image.open('sliceslice.jpg')
image.filter(ImageFilter.SHARPEN)
image.show()
print(pytesseract.image_to_string(image))
