from io import BytesIO
from typing import Optional, Tuple

from PIL import Image
from pdf2image import convert_from_bytes

from .accepted_types import PDF_FILE_TYPES, IMAGE_FILE_TYPES
from .download import documents_download
from ..url.is_valid import is_valid_url
from application.models.documents import Document


def document_input_processor(request) -> Tuple[Optional[list[Document]], dict, Optional[str]]:
    if request.files:
        documents: list[Document] = []
        data = {}
        for key in request.files.keys():
            file = request.files[key]
            content_type = file.content_type

            if content_type in PDF_FILE_TYPES:
                # convert pdf image
                file_stream = BytesIO(file.read())
                # Convert PDF pages to images
                pdf_images = convert_from_bytes(file_stream.getvalue())
                documents.append(
                    Document(id=key,images=pdf_images)
                )
            elif content_type in IMAGE_FILE_TYPES:
                # process the image file
                image = Image.open(file)
                documents.append(
                    Document(id=key,image=image)
                )
    elif request.is_json:
        request_data = request.get_json()
        url = request_data.get("url")
        if url is None or not isinstance(url, str) or url.strip() == "":
            return None, {}, "Could not find the value `url` in the body input."
        if not is_valid_url(url):
            return None, {}, f"The url value `{url}` is invalid"
        request_data.pop("url")
        data = dict(request_data)
        images = documents_download(url=url)
        documents = [
            Document(images=images)
        ]
    else:
        return None, {}, "No file or input data provided"

    if request.form:
        data.update(dict(request.form))

    return documents, data, None
