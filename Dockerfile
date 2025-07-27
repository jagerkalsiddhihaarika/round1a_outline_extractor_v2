# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . /app

# 🧠 Install Tesseract inside the container
RUN apt-get update && apt-get install -y tesseract-ocr

# 🧠 Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "run.py"]
