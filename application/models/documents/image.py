from typing import Optional

from pydantic import BaseModel

from PIL import Image


class DocumentPage:
    index: int
    image: Image
    extracted_text: Optional[str]

    def __init__(self, index:int, image: Image):
        self.index = index
        self.image = image
        self.extracted_text = None
