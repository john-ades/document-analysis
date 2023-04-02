from PIL import Image
import requests
from io import BytesIO

from .accepted_types import ACCEPTED_FILE_TYPES

def documents_download(url) -> list[Image]:
    response = requests.get(url, stream=True)

    content_type = response.headers['Content-Type']
    if content_type not in ACCEPTED_FILE_TYPES:
        raise ValueError("Invalid content type. Only PDF and image URLs are allowed.")

    if content_type == 'application/pdf':
        from pdf2image import convert_from_bytes

        # Convert the first page of the PDF to an image
        images = convert_from_bytes(response.content)
        if not images:
            raise ValueError("Could not convert PDF to image.")

    # If the URL is an image, directly load it into a Pillow Image object
    else:
        images = Image.open(BytesIO(response.content))

    return images
