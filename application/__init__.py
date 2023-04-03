import pytesseract
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    image = Image.open(file)
    text = pytesseract.image_to_string(image)

    return jsonify({"text": text})


if __name__ == '__main__':
    app.run()
