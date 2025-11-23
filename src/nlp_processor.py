"""
NLP module for intent detection using Hugging Face Transformers
"""
from typing import Dict, Optional, List
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch


class NLPProcessor:
    """Handles Natural Language Understanding and Intent Detection"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        """
        Initialize the NLP processor
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize intent classification pipeline
        try:
            self.intent_classifier = pipeline(
                "text-classification",
                model=model_name,
                device=0 if self.device == "cuda" else -1
            )
        except Exception as e:
            print(f"Error loading NLP model: {str(e)}")
            self.intent_classifier = None
        
        # Predefined intents (you can expand this)
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "farewell": ["goodbye", "bye", "see you", "thanks"],
            "account_inquiry": ["account", "balance", "details", "information"],
            "faq": ["what", "how", "where", "when", "why", "explain"],
            "support": ["help", "support", "assist", "issue", "problem"],
            "transaction": ["transaction", "transfer", "payment", "deposit", "withdraw"]
        }
    
    def detect_intent(self, text: str) -> Dict[str, any]:
        """
        Detect user intent from text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with intent and confidence score
        """
        if not self.intent_classifier:
            # Fallback to keyword-based intent detection
            return self._keyword_based_intent(text)
        
        try:
            # Use transformer model for intent classification
            result = self.intent_classifier(text)
            
            # Process result and match with predefined intents
            intent = self._match_intent(text)
            
            return {
                "intent": intent,
                "confidence": result[0]["score"] if isinstance(result, list) else 0.5,
                "text": text,
                "model_prediction": result
            }
        except Exception as e:
            print(f"Error in intent detection: {str(e)}")
            return self._keyword_based_intent(text)
    
    def _match_intent(self, text: str) -> str:
        """
        Match text with predefined intents using keyword matching
        
        Args:
            text: Input text
            
        Returns:
            Detected intent
        """
        text_lower = text.lower()
        
        # Score each intent
        intent_scores = {}
        for intent, keywords in self.intents.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            # Return intent with highest score
            return max(intent_scores, key=intent_scores.get)
        
        return "general"
    
    def _keyword_based_intent(self, text: str) -> Dict[str, any]:
        """
        Fallback keyword-based intent detection
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with intent and confidence
        """
        intent = self._match_intent(text)
        return {
            "intent": intent,
            "confidence": 0.7,
            "text": text
        }
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from text (can be extended with NER model)
        
        Args:
            text: Input text
            
        Returns:
            List of entities
        """
        # Placeholder for entity extraction
        # Can be extended with NER models like spaCy or transformers NER
        entities = []
        
        # Simple example: extract numbers (could be account numbers, amounts, etc.)
        import re
        numbers = re.findall(r'\d+', text)
        if numbers:
            entities.append({"type": "number", "value": numbers[0]})
        
        return entities

