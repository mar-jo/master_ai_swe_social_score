# Use Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy project files to the container
COPY . /app

# Set the PYTHONPATH to include the root directory
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Expose the application port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "SocialScores.main:app", "--host", "0.0.0.0", "--port", "8000"]
