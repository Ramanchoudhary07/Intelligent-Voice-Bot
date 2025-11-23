"""
Helper script to pre-download OpenAI Whisper model weights.

Whisper will automatically download model weights on first use. This script
loads the requested model to force the download ahead of time.

Note: Whisper requires `ffmpeg` to be installed on the system.
"""
import sys

try:
    import whisper
except Exception:
    print("Please install 'openai-whisper' before running this script: pip install openai-whisper")
    sys.exit(1)


def main(model_name: str = "small"):
    """Load Whisper model to ensure weights are downloaded."""
    print(f"Downloading (loading) Whisper model '{model_name}' — this may take a while...")
    try:
        model = whisper.load_model(model_name)
        print(f"Model '{model_name}' is ready.")
    except Exception as e:
        print(f"Error loading Whisper model '{model_name}': {e}")


if __name__ == "__main__":
    model = "small"
    if len(sys.argv) > 1:
        model = sys.argv[1]
    main(model)

