

# -------- builder: install deps in a clean layer --------
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System packages needed by reportlab (freetype, fonts, gs), and build tools for any wheels
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

# Copy requirement spec first to leverage Docker layer cache
COPY requirements.txt .

# Install Python deps into a local path to copy later
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "uvicorn[standard]" gunicorn

# -------- runtime: minimal image with only needed files --------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Runtime system deps for ReportLab rendering and fonts
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

# Copy application source
# If your code is under an "app" package folder, this keeps the same structure.
COPY . .

# Ensure the reports directory exists at runtime
RUN mkdir -p reports

# Expose the default app port (platforms like Render/Railway/Fly will set $PORT)
EXPOSE 8000

# Default environment variables (override in deploy with real secrets)
# Do NOT bake secrets into images; use platform secrets/vars.
ENV GROQ_API_URL="https://api.groq.com/openai/v1/chat/completions"

# Start Gunicorn with Uvicorn workers
# Adjust module path if needed:
# - If main.py is at repo root and defines `app = FastAPI()`, use "main:app"
# - If FastAPI app is app/main.py with `app = FastAPI()`, use "app.main:app"
ARG MODULE_PATH="app.main:app"
ENV MODULE_PATH=${MODULE_PATH}

# Bind to 0.0.0.0, use PORT if provided by platform
CMD exec gunicorn -k uvicorn.workers.UvicornWorker \
    ${MODULE_PATH} \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${WEB_CONCURRENCY:-2} \
    --timeout 120
