from flask import Blueprint, request, jsonify

from application.errors import APIError
from application.models.auto_tune_train_data import AutoTuneTrainData
from application.utils.documents.input_processor import document_input_processor

document_classification_api = Blueprint('document_classification', __name__)


@document_classification_api.route('/classification/document', methods=["POST"])
def parse_line_items():
    images, data, error = document_input_processor(request)
    if error:
        raise APIError(error)

    # run through auto_train
    # AutoTuneTrainData(prompt=,completion=)

    model_name = data.get("model_name")

    # run classification on each image

    return jsonify()
