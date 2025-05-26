import unittest
import sys
import os

# Add the parent directory to the sys.path to allow imports from sentiment_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_analyzer.analyzer import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    """
    Unit tests for the SentimentAnalyzer class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the SentimentAnalyzer instance once for all tests.
        This can also be used to ensure NLTK resources are ready if needed,
        though the analyzer class itself handles VADER download.
        """
        cls.analyzer = SentimentAnalyzer()

    def test_positive_sentiment(self):
        """Test a clearly positive text."""
        text = "This is a wonderful and excellent experience. I am very happy!"
        score = self.analyzer.analyze_sentiment(text)
        self.assertGreater(score, 0.5, "Score should be significantly positive.")
        self.assertTrue(-1.0 <= score <= 1.0, "Score should be within -1 to 1 range.")

    def test_negative_sentiment(self):
        """Test a clearly negative text."""
        text = "This is a terrible and awful situation. I am very sad."
        score = self.analyzer.analyze_sentiment(text)
        self.assertLess(score, -0.5, "Score should be significantly negative.")
        self.assertTrue(-1.0 <= score <= 1.0, "Score should be within -1 to 1 range.")

    def test_neutral_sentiment(self):
        """Test a relatively neutral text."""
        # VADER might still assign slight polarity, so we check for a score close to 0.
        text = "The report was published today."
        score = self.analyzer.analyze_sentiment(text)
        self.assertAlmostEqual(score, 0.0, delta=0.5, msg="Score should be close to neutral.")
        self.assertTrue(-1.0 <= score <= 1.0, "Score should be within -1 to 1 range.")

    def test_empty_string(self):
        """Test an empty string input."""
        text = ""
        score = self.analyzer.analyze_sentiment(text)
        self.assertEqual(score, 0.0, "Score for an empty string should be 0.0.")
        self.assertTrue(-1.0 <= score <= 1.0, "Score should be within -1 to 1 range.")

    def test_whitespace_string(self):
        """Test a string with only whitespace."""
        text = "   \t   \n  "
        score = self.analyzer.analyze_sentiment(text)
        self.assertEqual(score, 0.0, "Score for a whitespace-only string should be 0.0.")
        self.assertTrue(-1.0 <= score <= 1.0, "Score should be within -1 to 1 range.")
        
    def test_input_type_error(self):
        """Test non-string input type handling."""
        with self.assertRaises(TypeError):
            self.analyzer.analyze_sentiment(123) # type: ignore 
            # Using # type: ignore for static type checkers as we are intentionally passing wrong type

if __name__ == '__main__':
    unittest.main()
