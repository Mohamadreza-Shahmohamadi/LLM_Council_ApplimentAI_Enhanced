# Hugging Face Spaces compatible Dockerfile
FROM python:3.11-slim

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend requirements and install
COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && uv pip install --system -e .

# Copy frontend and build
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm ci && npm run build

# Copy backend
WORKDIR /app
COPY backend/ ./backend/
COPY main.py ./

# Create data directories
RUN mkdir -p data/conversations data/documents data/personalities

# Hugging Face Spaces uses port 7860
ENV PORT=7860
EXPOSE 7860

# Start command - serve both API and static frontend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
