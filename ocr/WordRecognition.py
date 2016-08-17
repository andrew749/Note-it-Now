import pytesseract
from PIL import Image
from PIL import ImageFilter

def get_string_from_file(path):
    image = Image.open(path)
    image.filter(ImageFilter.SHARPEN)
    # image.show()
    return pytesseract.image_to_string()
