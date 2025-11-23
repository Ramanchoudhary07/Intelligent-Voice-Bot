"""
Analytics Dashboard using Flask
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics import Analytics

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    """Render dashboard homepage"""
    return render_template("index.html")


@app.route("/api/analytics")
def get_analytics():
    """Get analytics data"""
    analytics = Analytics()
    summary = analytics.get_summary()
    return jsonify(summary)


@app.route("/api/metrics")
def get_metrics():
    """Get detailed metrics"""
    analytics = Analytics()
    metrics = analytics.get_metrics()
    return jsonify(metrics)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

