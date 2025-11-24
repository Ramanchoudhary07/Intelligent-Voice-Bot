# -------------------------------------------------
# Dockerfile for Intelligent Voice Bot (Render)
# -------------------------------------------------
# Use the official slim Python image (includes pip)
FROM python:3.11-slim

# ---- System dependencies -------------------------------------------------
# Install ffmpeg and any other native libs you need
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# ---- Working directory ----------------------------------------------------
WORKDIR /app

# ---- Copy source code ----------------------------------------------------
COPY requirements.txt .
COPY init_db.py .
COPY dashboard/ ./dashboard/
COPY src/ ./src/
COPY build.sh .

# ---- Install Python dependencies -------------------------------------------
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ---- Make sure the build script is executable (optional) -------------------
RUN chmod +x build.sh

# ---- Expose the port Render will assign (environment variable $PORT) ----------
EXPOSE 10000

# ---- Start command ---------------------------------------------------------
# Use the module runner so gunicorn works even if the binary isn’t on PATH
CMD ["sh", "-c", "python init_db.py && python -m gunicorn -w 4 -b 0.0.0.0:$PORT dashboard.app:app"]
