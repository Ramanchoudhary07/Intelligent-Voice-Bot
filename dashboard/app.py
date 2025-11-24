"""
Analytics Dashboard and API using Flask
"""
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import sys
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics import Analytics
from src.voice_bot import VoiceBot
from src.database import DatabaseManager
from config import settings

app = Flask(__name__)
# Allow CORS for frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure JWT
app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
jwt = JWTManager(app)

logger = logging.getLogger(__name__)

@app.route("/")
def index():
    """Render dashboard homepage (Legacy)"""
    return render_template("index.html")

# --- Auth Routes ---

@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
        
    db = DatabaseManager()
    if db.get_user_by_username(username):
        return jsonify({"error": "Username already exists"}), 400
        
    password_hash = generate_password_hash(password)
    if db.create_user(username, password_hash):
        access_token = create_access_token(identity=username)
        return jsonify({"message": "User created", "access_token": access_token}), 201
    else:
        return jsonify({"error": "Failed to create user"}), 500

@app.route("/api/login", methods=["POST"])
def login():
    """Login user"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
        
    db = DatabaseManager()
    user = db.get_user_by_username(username)
    
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token, "username": username}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/me", methods=["GET"])
@jwt_required()
def me():
    """Get current user info"""
    current_user = get_jwt_identity()
    return jsonify({"username": current_user}), 200

# --- Analytics Routes ---

@app.route("/api/analytics")
@jwt_required()
def get_analytics():
    """Get analytics data"""
    analytics = Analytics()
    summary = analytics.get_summary()
    return jsonify(summary)


@app.route("/api/metrics")
@jwt_required()
def get_metrics():
    """Get detailed metrics"""
    analytics = Analytics()
    metrics = analytics.get_metrics()
    return jsonify(metrics)

# --- Voice Bot Routes ---

@app.route('/api/submit_audio', methods=['POST'])
# @jwt_required() # Optional: protect voice bot too? Maybe keep open for demo or protect. Let's keep open for now or protect if user wants auth. User said "separating home page and dashboard with auth pages". Home page is voice bot. So maybe Home is public? Or Auth required?
# "separating home page and dashboard with auth pages" implies Auth is for Dashboard.
# Home page might be public. But "auth pages" implies you login to access the app.
# Let's assume Home is protected too, or at least Dashboard is.
# For now, I'll leave submit_audio unprotected for easier testing, or protect it if I want "Jarvis" to be personal.
# Let's protect it to be safe, as it uses resources.
# @jwt_required()
def submit_audio():
    """Accept an uploaded audio file, process it through the VoiceBot, and return response info."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        audio_file = request.files['file']
        if audio_file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        # Save uploaded file to a temporary location
        tmp_dir = Path(settings.base_dir) / 'tmp_uploads'
        tmp_dir.mkdir(parents=True, exist_ok=True)
        
        # Use a timestamp-based filename with proper extension
        import time
        timestamp = int(time.time() * 1000)
        # Browser MediaRecorder usually produces webm
        tmp_path = tmp_dir / f"recording_{timestamp}.webm"
        audio_file.save(str(tmp_path))
        
        logger.info(f"Saved uploaded audio to: {tmp_path}, size: {tmp_path.stat().st_size} bytes")

        # Process audio using VoiceBot
        bot = VoiceBot()
        output_path, error_msg = bot.process_audio_file(str(tmp_path))

        # Keep the file for debugging if it failed
        if output_path:
            try:
                tmp_path.unlink()
            except Exception:
                pass
        else:
            logger.error(f"Processing failed, keeping file at: {tmp_path}")

        if not output_path:
            return jsonify({"error": error_msg or "Processing failed"}), 500

        # Build URL for audio file
        # We need to return a full URL if frontend is on different port
        # Or just relative path if proxying.
        # Since we are using CORS, we should return full URL or relative to API.
        audio_url = url_for('serve_audio_file', filename=Path(output_path).name, _external=True)

        return jsonify({"audio_url": audio_url}), 200
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/audio/<path:filename>')
def serve_audio_file(filename: str):
    """Serve generated audio files from the configured audio directory."""
    audio_dir = str(settings.audio_dir)
    return send_from_directory(audio_dir, filename)


@app.route('/api/history')
@jwt_required()
def history():
    """Return recent query history from the database."""
    try:
        db = DatabaseManager()
        recent = db.get_recent_queries()
        return jsonify({"history": recent})
    except Exception as e:
        return jsonify({"history": [], "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
