# News Sentiment Analyzer

## Project Goal

This project aims to analyze sentiment in news articles over time to identify trends in the overall emotion of articles by year, month, week, etc.

## Minimal Viable Product (MVP)

The MVP will focus on setting up the core sentiment analysis functionality.

*   **Input:** Text content of a news article.
*   **Output:** A numerical sentiment score (e.g., ranging from -1.0 for very negative, 0 for neutral, to +1.0 for very positive).

## Current Capabilities (Phase 2)

The project can now perform the following:
*   **Fetch Recent News:** Utilizes the `pygooglenews` library to fetch up to 1000 recent news article titles along with their publication dates.
*   **Sentiment Analysis:** Processes the fetched titles through the `SentimentAnalyzer` (using NLTK's VADER) to calculate a sentiment score for each.
*   **Data Aggregation:** Employs `pandas` to aggregate sentiment scores, calculating the average daily sentiment.
*   **Visualization:** Generates two plots using `matplotlib`:
    *   A plot of individual sentiment scores for each news title over time (`individual_sentiment_plot.png`).
    *   A plot of the aggregated average daily sentiment scores over time (`daily_average_sentiment_plot.png`).
    These plots are saved as PNG files in the root directory when the analysis script is run.

## Future Goals (Post-MVP)

*   **Data Acquisition:** Implement methods to gather news articles (e.g., via news APIs, web scraping).
*   **Data Storage:** Choose and integrate a system for storing articles and their sentiment scores (e.g., database, CSV files).
*   **Temporal Analysis:** Develop capabilities to group, aggregate, and analyze sentiment scores by different timeframes (year, month, week).
*   **Advanced Sentiment:** Explore more nuanced emotional analysis beyond simple positive/negative/neutral.
*   **Visualization:** Create tools or scripts to visualize sentiment trends over time (e.g., line graphs, charts).
*   **Scalability:** Ensure the system can handle a growing volume of data.

## Initial Tech Stack

*   **Programming Language:** Python
*   **Core NLP Library:** An NLP library for sentiment analysis (e.g., NLTK with VADER, spaCy, or a Transformer-based model). The specific library for the MVP will be NLTK with VADER due to its simplicity and effectiveness for general sentiment.
*   **News Fetching:** `pygooglenews`
*   **Data Handling/Aggregation:** `pandas`
*   **Plotting:** `matplotlib`
*   **Testing:** Pytest or Python's built-in `unittest` framework.

## Modularity and Design

The project will be developed with a strong emphasis on Object-Oriented Programming (OOP) principles to ensure modularity and maintainability. Key components such as data input, sentiment processing, data storage, and analysis will be designed as distinct modules or classes.

## Contribution Guidelines

(Placeholder for contribution guidelines - to be added later.)

## License

(Placeholder for license - likely MIT License, to be confirmed and added later.)
