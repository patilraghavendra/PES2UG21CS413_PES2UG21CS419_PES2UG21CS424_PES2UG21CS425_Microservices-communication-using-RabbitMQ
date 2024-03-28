# Dockerfile for consumer_two microservice
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY item_creation.py .

CMD ["python", "item_creation.py"]

