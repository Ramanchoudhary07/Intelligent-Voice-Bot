#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install system dependencies
echo "Installing FFmpeg..."
apt-get update
apt-get install -y ffmpeg

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Verifying gunicorn installation..."
which gunicorn || echo "WARNING: gunicorn not found in PATH"

echo "Initializing database..."
python init_db.py || echo "Database initialization skipped (may already exist)"

echo "Build complete!"
