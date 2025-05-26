import nltk

# Attempt to download VADER lexicon if not already present.
# This is a common practice for NLTK resources.
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')
except LookupError: # Fallback for environments where find might not work as expected before download
    nltk.download('vader_lexicon')


from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    """
    A class to analyze the sentiment of a given text using NLTK's VADER.
    """

    def __init__(self):
        """
        Initializes the SentimentIntensityAnalyzer.
        """
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text: str) -> float:
        """
        Analyzes the sentiment of the provided text.

        Args:
            text: The string text to analyze.

        Returns:
            A float representing the compound sentiment score, ranging
            from -1.0 (most extreme negative) to +1.0 (most extreme positive).
            A score around 0.0 indicates neutrality.
        """
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")
        
        if not text.strip(): # Check if the string is empty or only whitespace
            # Return a neutral score for empty or whitespace-only text
            return 0.0

        # The scores dictionary contains 'neg', 'neu', 'pos', 'compound'
        # We will use the 'compound' score as it gives a single, normalized measure.
        scores = self.analyzer.polarity_scores(text)
        return scores['compound']
