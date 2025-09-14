# -------- builder: install deps in a clean layer --------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system deps for reportlab + fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    ghostscript \
    fonts-dejavu-core \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "uvicorn[standard]" gunicorn

# -------- runtime: minimal image --------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    ghostscript \
    fonts-dejavu-core \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed site-packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application source code
COPY . .

# Ensure reports directory exists
RUN mkdir -p reports

# Expose port (Render sets $PORT dynamically)
EXPOSE 8000

# Default envs (don’t bake secrets, override in Render dashboard)
ENV GROQ_API_URL="https://api.groq.com/openai/v1/chat/completions"

# App module path (adjust if your FastAPI app is elsewhere)
ARG MODULE_PATH="app.main:app"
ENV MODULE_PATH=${MODULE_PATH}

# Start app with Gunicorn + Uvicorn workers
CMD ["sh", "-c", "exec gunicorn -k uvicorn.workers.UvicornWorker \
    ${MODULE_PATH} \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${WEB_CONCURRENCY:-2} \
    --timeout 120"]
