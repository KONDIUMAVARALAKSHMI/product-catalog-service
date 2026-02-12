FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PostgreSQL if needed
RUN apt-get update && apt-get install -y \
    curl \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./test.db

EXPOSE 8000

CMD ["sh", "-c", "python src/seed.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
