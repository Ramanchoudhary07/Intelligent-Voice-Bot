#!/usr/bin/env bash
# -------------------------------------------------
# Build script for Render (and local dev)
# -------------------------------------------------
# Exit on any error (but we’ll handle a few known ones)
set -euo pipefail   # -e: abort on error, -u: undefined vars, -o pipefail: fail on pipeline errors

# ---------- Helper functions ----------
log() {
  echo -e "\033[1;34m[BUILD]\033[0m $*"
}

# ---------- System dependencies ----------
log "Updating package index..."
apt-get update -qq || { echo "apt-get update failed"; exit 1; }

log "Installing ffmpeg..."
apt-get install -y -qq ffmpeg || { echo "ffmpeg installation failed"; exit 1; }

# ---------- Python environment ----------
log "Upgrading pip..."
python3 -m pip install --upgrade pip

log "Installing Python dependencies..." 
python3 -m pip install -r requirements.txt

# ---------- Database initialization ----------
log "Running DB migrations / init..."
# If the DB already exists, [init_db.py](cci:7://file:///e:/D/Code/INTELLIGENT%20Voice%20bot/init_db.py:0:0-0:0) will just exit gracefully.
python3 init_db.py || { echo "Database init failed"; exit 1; }

log "Build script completed successfully."