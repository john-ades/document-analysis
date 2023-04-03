import uuid
from typing import Any

import PIL.Image
from pydantic import BaseModel

from PIL import Image

from .image import DocumentPage


class Document:
    id: str
    pages: list[DocumentPage]

    def __init__(self, id: str = None, image: Image.Image = None, images: list[Image.Image] = None):
        document_id = uuid.uuid4() if id is None else id
        document_id = str(document_id)
        document_images: list[Image.Image] = []
        if image:
            document_images = [image]
        if images:
            document_images = images

        if not all(isinstance(document_image, Image.Image) for document_image in document_images):
            raise ValueError("All images in array for Document.images must be of PIL.Image type.")

        self.id = document_id
        self.pages = [DocumentPage(index=idx, image=document_image) for idx, document_image in enumerate(document_images)]
