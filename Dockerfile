FROM python:3.12-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "SocialScores.main:app", "--host", "0.0.0.0", "--port", "8000"]
