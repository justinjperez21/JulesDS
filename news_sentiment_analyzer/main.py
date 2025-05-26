from sentiment_analyzer.analyzer import SentimentAnalyzer

def main():
    """
    Main function to demonstrate the SentimentAnalyzer.
    """
    analyzer = SentimentAnalyzer()

    sample_texts = [
        "This is a wonderfully fantastic and uplifting news article!",
        "The report highlights some deeply concerning and negative trends.",
        "The article presents a balanced view of the situation.",
        "It's a truly awful and terrible event.",
        "I am feeling very happy and joyful today.",
        "This is just a regular Tuesday.",
        "", # Empty string
        "   ", # String with only whitespace
    ]

    print("Sentiment Analysis MVP Test:")
    print("----------------------------")
    for text in sample_texts:
        score = analyzer.analyze_sentiment(text)
        print(f"Text: "{text}"")
        print(f"Sentiment Score: {score:.4f}
")

if __name__ == "__main__":
    main()
