FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install spacy language model
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000

# Use gunicorn for production instead of flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
