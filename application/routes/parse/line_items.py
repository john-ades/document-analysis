import json

from flask import Blueprint, request, jsonify

from pydantic import BaseModel

from application.errors import APIError
from application.models.line_item import LineItem
from application.models.price import Price
from application.services.llm import llm_completion
from application.services.ocr import extract_text
from application.static.prompts import \
    line_item_extraction_prompt, \
    line_item_extraction_w_context_prompt
from application.utils.documents.input_processor import document_input_processor

parse_line_items_api = Blueprint('parse_line_items', __name__)

CONTEXT_CHARACTER_LIMIT = 400


@parse_line_items_api.route('/parse/line_items', methods=["POST"])
def parse_line_items():
    documents, data, error = document_input_processor(request)
    if error:
        raise APIError(error)
    if len(documents) == 0:
        raise APIError("Could not find any documents or images to process")

    # get the input context
    context = data.get("context")
    if context is not None and (not isinstance(context, str) or len(context.strip()) > CONTEXT_CHARACTER_LIMIT):
        raise APIError(
            f"the `context` value must be a string and equal to or below {CONTEXT_CHARACTER_LIMIT} characters.")

    # extract text using OCR
    all_document_pages = []
    for document in documents:
        extracted_texts = [extract_text(page.image) for page in document.pages]
        for document_page, extracted_text in zip(document.pages, extracted_texts):
            document_page.extracted_text = extracted_text
            all_document_pages.append((document.id, document_page))

    # use gpt3 to get completion
    prompt_format = line_item_extraction_prompt if context is None else line_item_extraction_w_context_prompt
    prompts = [prompt_format.format_map({"<<DOCUMENT_TEXT>>": document_page.extracted_text, "<<CONTEXT>>": context}) for _, document_page in all_document_pages]

    completions = llm_completion(prompts)

    def extract_line_items(completion: str):
        rows = completion.strip().split("\n")
        rows = [[column.strip() for column in row[1:-1].strip().split("|")] for row in rows]

        line_items = []
        for row in rows:
            description = row[0]
            quantity = int(row[1]) if isinstance(row[1], int) else None
            try:
                price = Price(amount=row[2], currency_code=row[3])
            except ValueError:
                price = None
            line_items.append(LineItem(
                description=description,
                quantity=quantity,
                price=price
            ))
        return line_items

    class Response(BaseModel):
        document_id: str
        page: int
        text: str
        line_items: list[LineItem]

    responses = [
        Response(
            document_id=document_id,
            page=document_page.index,
            text=document_page.extracted_text,
            line_items=extract_line_items(completion)
        ) for (document_id, document_page), completion in zip(all_document_pages,completions)]

    return jsonify([
        json.loads(response.json()) for response in responses
    ]), 200
