"""
Speech-to-Text module using OpenAI Whisper
"""
import os
import tempfile
from typing import Optional

try:
    import whisper
    import torch
except Exception:
    whisper = None
    torch = None

from config import settings


class SpeechToText:
    """Handles speech-to-text conversion using OpenAI Whisper"""

    def __init__(self, model_name: str = "small", device: Optional[str] = None):
        """
        Initialize the Whisper model

        Args:
            model_name: Whisper model size to load (e.g., tiny, base, small, medium, large)
            device: Torch device string (e.g., 'cpu' or 'cuda'). If None, auto-detects.
        """
        if whisper is None:
            raise RuntimeError("Whisper package not installed. Please install 'openai-whisper' and ensure ffmpeg is available.")

        # Auto-select device if not provided
        if device is None:
            if torch is not None and torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"

        try:
            self.model = whisper.load_model(model_name, device=device)
            self.model_name = model_name
            self.device = device
        except Exception as e:
            print(f"Error loading Whisper model '{model_name}': {e}")
            raise

        # Buffer used for streaming-style transcription (simple append-to-temp-file approach)
        self._stream_temp_file = None

    def transcribe_audio_file(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe an audio file using Whisper. Whisper accepts many audio formats and will
        resample as needed via ffmpeg.

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text or None if transcription fails
        """
        try:
            if not os.path.exists(audio_file_path):
                print(f"Audio file not found: {audio_file_path}")
                return None

            # Whisper handles loading and resampling via ffmpeg
            result = self.model.transcribe(audio_file_path)
            return result.get("text", "").strip()
        except Exception as e:
            print(f"Error transcribing audio with Whisper: {e}")
            return None

    def transcribe_audio_bytes(self, audio_bytes: bytes, suffix: str = ".wav") -> Optional[str]:
        """
        Transcribe audio provided as bytes. Writes bytes to a temporary file then transcribes.

        Args:
            audio_bytes: Raw audio bytes (wav/mp3/etc.)
            suffix: File suffix to use when creating a temp file (default: .wav)

        Returns:
            Transcribed text or None
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            result = self.transcribe_audio_file(tmp_path)

            try:
                os.unlink(tmp_path)
            except Exception:
                pass

            return result
        except Exception as e:
            print(f"Error transcribing audio bytes with Whisper: {e}")
            return None

    def stream_transcribe(self, audio_chunk: bytes, finalize: bool = False) -> Optional[str]:
        """
        A simple streaming helper that appends incoming audio chunks to a temporary file
        and runs Whisper on the accumulated buffer. This is not real-time incremental
        streaming transcription, but provides a straightforward way to transcribe
        streaming input in this codebase.

        Args:
            audio_chunk: Chunk of audio bytes to append
            finalize: If True, run transcription and close the stream buffer

        Returns:
            Transcribed text when `finalize` is True, otherwise None
        """
        try:
            if self._stream_temp_file is None:
                self._stream_temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)

            # Append chunk to temp file
            with open(self._stream_temp_file.name, 'ab') as f:
                f.write(audio_chunk)

            if finalize:
                result = self.transcribe_audio_file(self._stream_temp_file.name)
                try:
                    os.unlink(self._stream_temp_file.name)
                except Exception:
                    pass
                self._stream_temp_file = None
                return result

            return None
        except Exception as e:
            print(f"Error in stream transcription with Whisper: {e}")
            return None
