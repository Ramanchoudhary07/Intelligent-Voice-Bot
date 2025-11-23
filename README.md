# Intelligent Voice Bot

Develop an intelligent voice bot capable of handling basic customer queries and interactions, leveraging advanced AI technologies like Natural Language Processing (NLP), Speech-to-Text, and Text-to-Speech systems.

## Key Features

- **Speech to Text Conversion**

  - Uses speech recognition systems
  - Powered by OpenAI Whisper (via the `openai-whisper` package)

- **Natural Language Understanding**

  - Processes text input to understand user intent
  - Utilizes Hugging Face Transformers

- **Response Generation**

  - Employs pre-trained language models to generate responses
  - Integrates with Google Gemini API (free tier available)

- **Text to Speech Conversion**

  - Converts generated response to speech
  - Uses Amazon Polly API

- **Integration with Backend/Database**

  - Connects to backend services or databases
  - Allows retrieval of account details or FAQs

- **Analytics Dashboard**
  - Tracks and displays user queries, response time, and error rates

## Technical Architecture

-- **Speech Input** → **Speech Recognition (OpenAI Whisper)** → **NLP Intent Detection** → **Response Generation (Google Gemini API)** → **Speech Output (Text-to-Speech)**

- **Backend Integration** for fetching account and FAQ details
- **Analytics Dashboard** for monitoring bot performance

## Setup & Usage

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free tier available)
- AWS account with Amazon Polly access (for text-to-speech)
- OpenAI Whisper (models will download automatically when first used) and `ffmpeg` installed on your system
- (Optional) PostgreSQL or MongoDB database

### Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **(Optional) Pre-download Whisper model weights:**

   Whisper downloads model weights on first use. To pre-download a model (for example `small`), run:

   ```bash
   python download_deepspeech_models.py small
   ```

   Note: `ffmpeg` must be installed on the system for Whisper to process audio files. On Windows you can install https://ffmpeg.org/ and ensure the binary is on your `PATH`.

6. **Configure environment variables:**

   ```bash
   # Copy the example environment file
   copy env.example .env  # Windows
   # or
   cp env.example .env    # macOS/Linux
   ```

   Edit `.env` and add your API keys:

   - `GEMINI_API_KEY`: Your Google Gemini API key (get free API key from Google AI Studio)
   - `AWS_ACCESS_KEY_ID`: Your AWS access key ID
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key
   - `AWS_REGION`: AWS region (default: us-east-1)
   - (Optional) Database and backend configuration

### Usage

#### Basic Usage

**Process an audio file:**

```bash
python main.py --audio path/to/audio.wav
```

**Process a text query (for testing):**

```bash
python main.py --text "Hello, how can I help you?"
```

**Interactive mode:**

```bash
python main.py
```

Then type your queries interactively.

**View analytics:**

```bash
python main.py --analytics
```

#### Start Analytics Dashboard

1. **Navigate to dashboard directory:**

   ```bash
   cd dashboard
   ```

2. **Run the Flask app:**

   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to `http://localhost:5000`

### Project Structure

```
INTELLIGENT Voice bot/
├── src/
│   ├── __init__.py
│   ├── speech_to_text.py      # Speech-to-Text module
│   ├── nlp_processor.py        # NLP and intent detection
│   ├── response_generator.py   # Response generation (OpenAI)
│   ├── text_to_speech.py       # Text-to-Speech module
│   ├── database.py             # Database integration
│   ├── analytics.py            # Analytics tracking
│   └── voice_bot.py            # Main bot orchestrator
├── dashboard/
│   ├── app.py                  # Flask dashboard app
│   └── templates/
│       └── index.html          # Dashboard UI
├── audio_files/                # Generated audio files (auto-created)
├── logs/                       # Log files (auto-created)
├── analytics_data/             # Analytics data (auto-created)
├── config.py                   # Configuration management
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

### API Setup

1. **Google Gemini API (for Response Generation):**

   - Get your free API key from https://makersuite.google.com/app/apikey
   - Or visit https://aistudio.google.com/app/apikey
   - Add it to `.env` as `GEMINI_API_KEY`
   - Free tier includes generous usage limits

2. **OpenAI Whisper (for Speech-to-Text):**

   - Whisper models are provided by OpenAI and are downloaded automatically on first use by the `openai-whisper` package
   - Ensure `ffmpeg` is installed on your system (Whisper uses ffmpeg for audio decoding/resampling)
   - Optionally pre-download a model using `python download_deepspeech_models.py <model_name>` (for example `small`)

3. **Amazon Polly (for Text-to-Speech):**

   - Sign up for AWS account at https://aws.amazon.com/
   - Create IAM user with Amazon Polly permissions
   - Get your Access Key ID and Secret Access Key
   - Add to `.env` as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
   - Set `AWS_REGION` (default: us-east-1)

4. **Hugging Face (Optional):**
   - Models are downloaded automatically on first use
   - Add token to `.env` if using private models

### Database Setup (Optional)

For PostgreSQL:

```bash
# Install PostgreSQL and create database
createdb voicebot_db

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/voicebot_db
```

For MongoDB:

```bash
# Install MongoDB and update .env
MONGO_URI=mongodb://localhost:27017/voicebot_db
DATABASE_TYPE=mongodb
```

### Troubleshooting

- **Audio processing issues:** Ensure audio files are in WAV format with 16kHz sample rate, mono channel, 16-bit
- **Whisper audio/model issues:** Ensure `ffmpeg` is installed and available on your PATH. Whisper model weights are downloaded automatically on first use; run `python download_deepspeech_models.py small` to pre-download the `small` model if desired.
- **API errors:** Verify all API keys are correctly set in `.env`
- **Import errors:** Make sure virtual environment is activated and all dependencies are installed
