FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly (without editable install)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
        "fastapi[standard]>=0.104.0" \
        "uvicorn[standard]>=0.24.0" \
        "pydantic>=2.0.0" \
        "google-genai>=0.2.0" \
        "python-multipart>=0.0.6" \
        "python-dotenv>=1.0.0"

# Copy application code from backend/ (build context root) to /app/backend/
# This maintains the import structure (backend.main, backend.routers, etc.)
COPY . ./backend/

# Note: .env file is NOT copied into the image
# Environment variables are provided via docker-compose.yml (see environment section)
# The application's load_dotenv() will use environment variables if .env is missing

# Create directory for generated videos
RUN mkdir -p backend/generated_videos

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
