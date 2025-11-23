"""
Response generation module using Google Gemini API
"""
import os
from typing import Dict, Optional
# import google.generativeai as genai
from google import genai
from config import settings


class ResponseGenerator:
    """Handles response generation using Google Gemini API"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key not found in environment variables")
        # client = genai.Client(api_key=settings.gemini_api_key)
        # genai.configure(api_key=settings.gemini_api_key)
        # print(f"Gemini API key: {settings.gemini_api_key}")
        # models = client.list_models()
        # model_names = [model.display_name for model in models]
        # print(f"Available models: {model_names}")
        # self.model = genai.GenerativeModel('gemini-2.5-flash-preview-native-audio-dialog-2025-05-19')
        self.client = genai.Client(api_key=settings.gemini_api_key)


    
    def generate_response(
        self,
        user_query: str,
        intent: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate a response based on user query and intent
        
        Args:
            user_query: The user's query text
            intent: Detected intent
            context: Additional context (e.g., account info, FAQs)
            
        Returns:
            Generated response text
        """
        try:
            # Build system prompt based on intent
            system_prompt = self._build_system_prompt(intent, context)
            
            # Combine system prompt and user query
            full_prompt = f"{system_prompt}\n\nUser: {user_query}\nAssistant:"
            print(f"Full prompt: {full_prompt}")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            # print(f"Response: {response}")
            # print("CONTROLLED REACHED HERE")
            return response.text.strip()
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return self._fallback_response(intent)
    
    def _build_system_prompt(self, intent: str, context: Optional[Dict]) -> str:
        """
        Build system prompt based on intent
        
        Args:
            intent: Detected intent
            context: Additional context
            
        Returns:
            System prompt string
        """
        base_prompt = "You are a helpful and friendly customer service voice assistant."
        
        intent_prompts = {
            "greeting": "Respond warmly to the greeting and ask how you can help.",
            "farewell": "Thank the user and wish them well.",
            "account_inquiry": "Provide helpful information about account-related queries. Be concise and clear.",
            "faq": "Answer frequently asked questions clearly and helpfully.",
            "support": "Offer support and assistance. If you cannot resolve the issue, guide them to human support.",
            "transaction": "Assist with transaction-related queries. Be careful with sensitive information."
        }
        
        prompt = f"{base_prompt} {intent_prompts.get(intent, 'Provide helpful assistance.')}"
        
        if context:
            if "account_info" in context:
                prompt += f"\nAccount Information: {context['account_info']}"
            if "faqs" in context:
                prompt += f"\nRelevant FAQs: {context['faqs']}"
        
        return prompt
    
    def _fallback_response(self, intent: str) -> str:
        """
        Fallback response if API call fails
        
        Args:
            intent: Detected intent
            
        Returns:
            Fallback response text
        """
        fallback_responses = {
            "greeting": "Hello! How can I assist you today?",
            "farewell": "Thank you for contacting us. Have a great day!",
            "account_inquiry": "I can help you with account information. Please provide more details.",
            "faq": "I'm here to answer your questions. What would you like to know?",
            "support": "I'm here to help. Please describe the issue you're experiencing.",
            "transaction": "I can assist with transaction-related queries. How can I help?",
            "general": "I'm here to help. Could you please provide more details?"
        }
        
        return fallback_responses.get(intent, "I'm here to assist you. How can I help?")
