from flask import Flask

from application.errors import api_error_blueprint
from application.routes.classification.document import document_classification_api
from application.routes.parse.line_items import parse_line_items_api


def create_app():
    app = Flask(__name__)

    # Register error blueprint
    app.register_blueprint(api_error_blueprint)

    # Register Routes
    app.register_blueprint(document_classification_api)
    app.register_blueprint(parse_line_items_api)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
