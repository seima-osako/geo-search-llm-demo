# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV CHAINLIT_SERVER_PORT=8000
ENV HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app_self-query.py .
COPY setting.py .
COPY prompts.py .
COPY .env .
COPY chainlit.md .

# Copy ChromaDB directory
COPY chroma_db/ ./chroma_db/

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["chainlit", "run", "app_self-query.py", "--port", "8000", "--host", "0.0.0.0"]