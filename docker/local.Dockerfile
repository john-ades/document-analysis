# Use the clearlinux/tesseract-ocr base image
FROM clearlinux/tesseract-ocr:latest

# Set the working directory
WORKDIR /app

# Install required packages for Flask and update pip
RUN swupd bundle-add python3-basic && \
    pip install --upgrade pip

# Install library dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the Flask application file into the container
COPY /application .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Expose the port Flask is running on
EXPOSE 5000

# Start the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]