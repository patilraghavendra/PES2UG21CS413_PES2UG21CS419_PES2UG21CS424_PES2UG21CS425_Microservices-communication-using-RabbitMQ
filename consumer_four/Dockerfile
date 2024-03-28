# Dockerfile for consumer_four microservice
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY order_processing.py .

CMD ["python", "order_processing.py"]
