"""
Text-to-Speech module using Amazon Polly
"""
import os
from typing import Optional
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from config import settings


class TextToSpeech:
    """Handles text-to-speech conversion using Amazon Polly"""
    
    def __init__(self, voice_id: str = "Joanna", region_name: str = "us-east-1"):
        """
        Initialize the Amazon Polly client
        
        Args:
            voice_id: Amazon Polly voice ID (e.g., "Joanna", "Matthew", "Amy")
            region_name: AWS region name
        """
        try:
            # Initialize AWS credentials from environment or config
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID") or settings.aws_access_key_id
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY") or settings.aws_secret_access_key
            
            if not aws_access_key_id or not aws_secret_access_key:
                print("Warning: AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            
            self.polly_client = boto3.client(
                'polly',
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
            
            self.voice_id = voice_id
            self.region_name = region_name
        except Exception as e:
            print(f"Error initializing Amazon Polly client: {str(e)}")
            self.polly_client = None
    
    def synthesize(self, text: str, output_file: Optional[str] = None, output_format: str = "mp3") -> Optional[bytes]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            output_file: Optional path to save the audio file
            output_format: Output format (mp3, ogg_vorbis, pcm)
            
        Returns:
            Audio data as bytes, or None if synthesis fails
        """
        if not self.polly_client:
            print("Polly client not initialized")
            return None
        
        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat=output_format,
                VoiceId=self.voice_id,
                Engine='neural'  # Use neural engine for better quality
            )
            
            audio_data = response['AudioStream'].read()
            
            # Save to file if output path is provided
            if output_file:
                with open(output_file, "wb") as out:
                    out.write(audio_data)
                print(f"Audio saved to {output_file}")
            
            return audio_data
        except (BotoCoreError, ClientError) as e:
            print(f"Error synthesizing speech: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
    
    def list_voices(self, language_code: str = "en-US") -> list:
        """
        List available voices
        
        Args:
            language_code: Language code to filter voices (e.g., "en-US")
            
        Returns:
            List of available voice IDs
        """
        if not self.polly_client:
            return []
        
        try:
            response = self.polly_client.describe_voices(LanguageCode=language_code)
            return [voice['Id'] for voice in response['Voices']]
        except (BotoCoreError, ClientError) as e:
            print(f"Error listing voices: {str(e)}")
            return []
    
    def set_voice(self, voice_id: str):
        """
        Change the voice
        
        Args:
            voice_id: Name of the voice to use (e.g., "Joanna", "Matthew")
        """
        self.voice_id = voice_id
    
    def get_voice_info(self, voice_id: Optional[str] = None) -> Optional[dict]:
        """
        Get information about a specific voice
        
        Args:
            voice_id: Voice ID to get info for (defaults to current voice)
            
        Returns:
            Dictionary with voice information or None
        """
        if not self.polly_client:
            return None
        
        voice_to_check = voice_id or self.voice_id
        
        try:
            response = self.polly_client.describe_voices()
            for voice in response['Voices']:
                if voice['Id'] == voice_to_check:
                    return {
                        'Id': voice['Id'],
                        'LanguageCode': voice['LanguageCode'],
                        'LanguageName': voice['LanguageName'],
                        'Gender': voice['Gender'],
                        'SupportedEngines': voice.get('SupportedEngines', [])
                    }
            return None
        except (BotoCoreError, ClientError) as e:
            print(f"Error getting voice info: {str(e)}")
            return None
