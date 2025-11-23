"""
Main Voice Bot class that orchestrates all components
"""
import time
from typing import Optional
from src.speech_to_text import SpeechToText
from src.nlp_processor import NLPProcessor
from src.response_generator import ResponseGenerator
from src.text_to_speech import TextToSpeech
from src.database import DatabaseManager
from src.analytics import Analytics
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceBot:
    """Main Voice Bot class"""
    
    def __init__(self):
        """Initialize the Voice Bot with all components"""
        logger.info("Initializing Voice Bot...")
        
        # Initialize components
        try:
            self.speech_to_text = SpeechToText()
            logger.info("Speech-to-Text initialized")
        except Exception as e:
            logger.error(f"Error initializing Speech-to-Text: {str(e)}")
            self.speech_to_text = None
        
        try:
            self.nlp_processor = NLPProcessor()
            logger.info("NLP Processor initialized")
        except Exception as e:
            logger.error(f"Error initializing NLP Processor: {str(e)}")
            self.nlp_processor = None
        
        try:
            self.response_generator = ResponseGenerator()
            logger.info("Response Generator initialized")
        except Exception as e:
            logger.error(f"Error initializing Response Generator: {str(e)}")
            self.response_generator = None
        
        try:
            self.text_to_speech = TextToSpeech()
            logger.info("Text-to-Speech initialized")
        except Exception as e:
            logger.error(f"Error initializing Text-to-Speech: {str(e)}")
            self.text_to_speech = None
        
        self.database = DatabaseManager()
        self.analytics = Analytics()
        
        logger.info("Voice Bot initialization complete")
    
    def process_audio_file(self, audio_file_path: str) -> Optional[str]:
        """
        Process an audio file through the complete pipeline
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            Path to the output audio file with response, or None if processing fails
        """
        start_time = time.time()
        
        try:
            # Step 1: Speech-to-Text
            logger.info(f"Processing audio file: {audio_file_path}")
            if not self.speech_to_text:
                logger.error("Speech-to-Text not available")
                return None
            
            transcribed_text = self.speech_to_text.transcribe_audio_file(audio_file_path)
            if not transcribed_text:
                logger.error("Failed to transcribe audio")
                return None
            
            logger.info(f"Transcribed text: {transcribed_text}")
            
            # Step 2: NLP Intent Detection
            if not self.nlp_processor:
                logger.error("NLP Processor not available")
                return None
            
            intent_data = self.nlp_processor.detect_intent(transcribed_text)
            intent = intent_data.get("intent", "general")
            logger.info(f"Detected intent: {intent}")
            
            # Step 3: Get context from database/backend if needed
            context = {}
            if intent in ["account_inquiry", "transaction"]:
                # Extract account ID if present
                entities = self.nlp_processor.extract_entities(transcribed_text)
                for entity in entities:
                    if entity.get("type") == "number":
                        account_info = self.database.get_account_info(entity["value"])
                        if account_info:
                            context["account_info"] = account_info
                        break
            
            if intent == "faq":
                faqs = self.database.get_faqs(transcribed_text)
                if faqs:
                    context["faqs"] = faqs
            
            # Step 4: Generate Response
            if not self.response_generator:
                logger.error("Response Generator not available")
                return None
            
            response_text = self.response_generator.generate_response(
                transcribed_text,
                intent,
                context
            )
            logger.info(f"Generated response: {response_text}")
            
            # Step 5: Text-to-Speech
            if not self.text_to_speech:
                logger.error("Text-to-Speech not available")
                return None
            
            output_file = settings.audio_dir / f"response_{int(time.time())}.mp3"
            audio_data = self.text_to_speech.synthesize(response_text, str(output_file))
            
            if not audio_data:
                logger.error("Failed to synthesize speech")
                return None
            
            # Calculate response time
            response_time = int((time.time() - start_time) * 1000)
            
            # Step 6: Log to database
            self.database.log_query(
                transcribed_text,
                intent,
                response_text,
                response_time
            )
            
            # Step 7: Track analytics
            self.analytics.track_query(
                transcribed_text,
                intent,
                response_time,
                success=True
            )
            
            logger.info(f"Processing complete in {response_time}ms")
            return str(output_file)
        
        except Exception as e:
            logger.error(f"Error processing audio file: {str(e)}")
            response_time = int((time.time() - start_time) * 1000)
            
            # Log error
            self.database.log_query(
                audio_file_path,
                "error",
                "",
                response_time,
                error=str(e)
            )
            
            self.analytics.track_query(
                audio_file_path,
                "error",
                response_time,
                success=False,
                error=str(e)
            )
            
            return None
    
    def process_text_query(self, text: str) -> tuple[str, Optional[str]]:
        """
        Process a text query (useful for testing without audio)
        
        Args:
            text: Input text query
            
        Returns:
            Tuple of (response_text, audio_file_path)
        """
        start_time = time.time()
        
        try:
            # NLP Intent Detection
            if not self.nlp_processor:
                logger.error("NLP Processor not available")
                return "Error: NLP Processor not initialized. Please check your configuration.", None
            
            intent_data = self.nlp_processor.detect_intent(text)
            intent = intent_data.get("intent", "general")
            logger.info(f"Detected intent: {intent}")
            
            # Get context
            context = {}
            if intent in ["account_inquiry", "transaction"]:
                entities = self.nlp_processor.extract_entities(text)
                for entity in entities:
                    if entity.get("type") == "number":
                        account_info = self.database.get_account_info(entity["value"])
                        if account_info:
                            context["account_info"] = account_info
                        break
            
            # Generate Response
            if not self.response_generator:
                logger.error("Response Generator not available")
                return "Error: Response Generator not initialized. Please check your OpenAI API key in .env file.", None
            
            response_text = self.response_generator.generate_response(text, intent, context)
            
            # Text-to-Speech
            output_file = settings.audio_dir / f"response_{int(time.time())}.mp3"
            audio_file_path = None
            if self.text_to_speech:
                self.text_to_speech.synthesize(response_text, str(output_file))
                audio_file_path = str(output_file)
            
            # Log and track
            response_time = int((time.time() - start_time) * 1000)
            self.database.log_query(text, intent, response_text, response_time)
            self.analytics.track_query(text, intent, response_time, success=True)
            
            return response_text, audio_file_path
        
        except Exception as e:
            logger.error(f"Error processing text query: {str(e)}")
            response_time = int((time.time() - start_time) * 1000)
            self.analytics.track_query(text, "error", response_time, success=False, error=str(e))
            return f"Error: {str(e)}", None

