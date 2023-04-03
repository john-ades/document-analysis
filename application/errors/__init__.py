from flask import Blueprint, jsonify

api_error_blueprint = Blueprint('error_blueprint', __name__)


class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


@api_error_blueprint.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response
