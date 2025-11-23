# Quick Start Guide

## Fast Setup (5 minutes)

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Pre-download Whisper model weights

Whisper downloads model weights automatically on first use. You can pre-download a model (for example `small`) with:

```bash
python download_deepspeech_models.py small
```

Note: Install `ffmpeg` on your system and make sure the binary is on your `PATH` for Whisper to process audio.

### 4. Configure Environment Variables

Copy `env.example` to `.env` and update with your API keys:

```bash
copy env.example .env  # Windows
# or
cp env.example .env    # macOS/Linux
```

Required API keys:

- `GEMINI_API_KEY`: Your Google Gemini API key (free tier available)
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
- `AWS_REGION`: AWS region (default: us-east-1)

### 5. Test the Bot

```bash
python main.py --text "Hello, how can you help me?"
```

### 6. (Optional) Start Analytics Dashboard

```bash
cd dashboard
python app.py
```

Then open http://localhost:5000 in your browser.

## Getting API Keys

### Google Gemini Setup (for Response Generation)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) or [MakerSuite](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy the API key
5. Add to `.env`: `GEMINI_API_KEY=your-api-key-here`
6. Note: Free tier includes generous usage limits

### OpenAI Whisper Setup (for Speech-to-Text)

1. Whisper model weights are downloaded automatically on first use by the `openai-whisper` package
2. Ensure `ffmpeg` is installed on your system and available on your `PATH`
3. Optionally pre-download a model with `python download_deepspeech_models.py <model_name>` (for example `small`)

### Amazon Polly Setup (for Text-to-Speech)

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Sign in or create an AWS account
3. Navigate to **IAM** (Identity and Access Management)
4. Create a new IAM user:
   - Go to **Users** → **Add users**
   - Set username and select "Programmatic access"
   - Attach policy: **AmazonPollyFullAccess** (or create custom policy with Polly permissions)
   - Save the **Access Key ID** and **Secret Access Key**
5. Add to `.env`:
   - `AWS_ACCESS_KEY_ID=your-access-key-id`
   - `AWS_SECRET_ACCESS_KEY=your-secret-access-key`
   - `AWS_REGION=us-east-1` (or your preferred region)

## Common Commands

- **Text query**: `python main.py --text "your query"`
- **Audio file**: `python main.py --audio path/to/audio.wav`
- **Interactive mode**: `python main.py`
- **Analytics**: `python main.py --analytics`

## Troubleshooting

- **Import errors**: Make sure virtual environment is activated
- **API errors**: Check that API keys are correctly set in `.env`
- **Audio errors**: Ensure audio files are in WAV format, 16kHz sample rate, mono channel, 16-bit
- **Whisper errors**: Ensure `ffmpeg` is installed and available on your PATH. Whisper model weights download automatically; run `python download_deepspeech_models.py small` to pre-download if needed.
