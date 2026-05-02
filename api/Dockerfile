
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY main.py .

ENV PORT=8080
ENV GCS_BUCKET_NAME=mon-bucket-api
ENV GCS_FILE_PATH=data/entries.json
ENV GCP_PROJECT_ID=mon-projet-gcp
ENV GCP_REGION=us-central1

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "main:app"]
