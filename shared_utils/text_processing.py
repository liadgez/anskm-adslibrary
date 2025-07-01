"""
Shared Text Processing Utilities
===============================

Common text processing functions extracted from multiple components
to eliminate duplication and ensure consistency.
"""

import re
import string
from typing import List, Dict, Any, Optional


class TextProcessor:
    """Shared text processing and normalization utilities."""
    
    def __init__(self):
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", 
            flags=re.UNICODE
        )
        
    def clean_text(self, text: str, remove_emojis: bool = False) -> str:
        """
        Clean and normalize text for analysis.
        
        Args:
            text: Raw text to clean
            remove_emojis: Whether to remove emoji characters
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
            
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove emojis if requested
        if remove_emojis:
            text = self.emoji_pattern.sub('', text)
            
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_features(self, text: str) -> Dict[str, Any]:
        """
        Extract linguistic features from text.
        
        Args:
            text: Cleaned text
            
        Returns:
            Dictionary of extracted features
        """
        features = {}
        
        # Basic metrics
        features['word_count'] = len(text.split())
        features['char_count'] = len(text)
        features['sentence_count'] = len([s for s in text.split('.') if s.strip()])
        
        # Capitalization patterns
        features['all_caps_words'] = len(re.findall(r'\b[A-Z]{3,}\b', text))
        features['caps_ratio'] = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        
        # Punctuation analysis
        features['exclamation_count'] = text.count('!')
        features['question_count'] = text.count('?')
        features['emoji_count'] = len(self.emoji_pattern.findall(text))
        
        # Numeric content
        features['number_count'] = len(re.findall(r'\d+', text))
        features['percentage_mentions'] = len(re.findall(r'\d+%', text))
        features['price_mentions'] = len(re.findall(r'\$\d+', text))
        
        # Call-to-action indicators
        cta_patterns = [
            r'\b(shop|buy|get|try|learn|discover|sign up|download)\b',
            r'\b(now|today|click|tap|visit)\b'
        ]
        features['cta_signals'] = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                                    for pattern in cta_patterns)
        
        return features
    
    def extract_buzzwords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract potential buzzwords from text.
        
        Args:
            text: Text to analyze
            min_length: Minimum word length to consider
            
        Returns:
            List of potential buzzwords
        """
        # Remove punctuation and convert to lowercase
        clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        words = clean_text.split()
        
        # Filter by length and remove common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        buzzwords = [word for word in words 
                    if len(word) >= min_length and word not in common_words]
        
        return list(set(buzzwords))  # Remove duplicates
    
    def extract_cta_text(self, text: str) -> List[str]:
        """
        Extract call-to-action phrases from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of CTA phrases found
        """
        cta_patterns = [
            r'\b(shop now|buy today|get started|learn more|sign up|download)\b',
            r'\b(click here|tap to|visit us|try free|order now)\b',
            r'\b(limited time|act now|don\'t miss|hurry up)\b'
        ]
        
        ctas = []
        for pattern in cta_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ctas.extend(matches)
        
        return ctas
    
    def analyze_sentiment_indicators(self, text: str) -> Dict[str, int]:
        """
        Analyze sentiment indicators in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment indicator counts
        """
        positive_patterns = [
            r'\b(amazing|awesome|great|excellent|perfect|love|best)\b',
            r'\b(incredible|fantastic|wonderful|outstanding|brilliant)\b'
        ]
        
        negative_patterns = [
            r'\b(terrible|awful|worst|hate|horrible|bad)\b',
            r'\b(disappointing|frustrating|annoying|poor)\b'
        ]
        
        urgency_patterns = [
            r'\b(urgent|immediate|asap|quickly|fast|rapid)\b',
            r'\b(deadline|expires|limited|ending|final)\b'
        ]
        
        return {
            'positive_count': sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                                for pattern in positive_patterns),
            'negative_count': sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                                for pattern in negative_patterns),
            'urgency_count': sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                               for pattern in urgency_patterns)
        }


# Convenience functions for backward compatibility
def clean_text(text: str, remove_emojis: bool = False) -> str:
    """Convenience function for text cleaning."""
    processor = TextProcessor()
    return processor.clean_text(text, remove_emojis)


def extract_features(text: str) -> Dict[str, Any]:
    """Convenience function for feature extraction."""
    processor = TextProcessor()
    return processor.extract_features(text)