import json

from flask import Blueprint, request, jsonify

from pydantic import BaseModel

from application.errors import APIError
from application.utils.strings.input_parse import str_input_parse
from application.services.ocr import extract_text
from application.services.classification.images.zero_shot import zero_shot_image_classification
from application.utils.strings.is_alnum_space_or_underscore import is_alpha_num_space_or_underscore
from application.utils.documents.input_processor import document_input_processor

document_classification_api = Blueprint('document_classification', __name__)

UNKNOWN_CLASS = "unknown"


@document_classification_api.route('/classification/document', methods=["POST"])
def document_classification():
    documents, data, error = document_input_processor(request)
    if error:
        raise APIError(error)

    model_name = data.get("model_name")
    if model_name is not None and not isinstance(model_name, str):
        raise APIError("Could not read model name")

    predict_classes = data.get("classes")
    if predict_classes is not None:
        predict_classes = str_input_parse(predict_classes)

    context = data.get("context")
    if context is not None and (not isinstance(context, str) or len(context.strip()) > CONTEXT_CHARACTER_LIMIT):
        raise APIError(
            f"The `context` value must be a string and equal to or below {CONTEXT_CHARACTER_LIMIT} characters.")

    if predict_classes is not None:
        if len(predict_classes) == 0:
            raise APIError("Must contain at least one class")

    # ensure each class is only alphanumeric characters
    all_classes_valid = all(is_alpha_num_space_or_underscore(predict_class) for predict_class in predict_classes)
    if not all_classes_valid:
        raise APIError("Classes can only contain alpha numeric, space, or underscore characters.")

    # extract text using OCR
    all_document_pages = []
    for document in documents:
        extracted_texts = [extract_text(page.image) for page in document.pages]
        for document_page, extracted_text in zip(document.pages, extracted_texts):
            document_page.extracted_text = extracted_text
            all_document_pages.append((document.id, document_page))

    # use zero shot text classification
    predictions = zero_shot_image_classification(images=[doc_page[1].image for doc_page in all_document_pages],classes=predict_classes)

    class Response(BaseModel):
        document_id: str
        page: int
        predicted_classes: dict[str, float]

    responses = [
        Response(
            document_id=document_page[0],
            page=document_page[1].index,
            predicted_classes=scores
        )
        for document_page, scores in zip(all_document_pages, predictions)]

    return jsonify([
        json.loads(response.json()) for response in responses
    ]), 200
