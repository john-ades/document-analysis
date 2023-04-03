import pytesseract
from PIL import Image

TESSERACT_CONFIG = r'-c load_system_dawg=0 -c load_freq_dawg=0'


def extract_text(image: Image) -> str:
    """
    Optical Character Recognition Task:
        Takes an image and returns a str of all the text
    """
    return pytesseract.image_to_string(image, config=TESSERACT_CONFIG)
