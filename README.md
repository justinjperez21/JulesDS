# News Sentiment Analyzer

## Project Goal

This project aims to analyze sentiment in news articles over time to identify trends in the overall emotion of articles by year, month, week, etc., by fetching and processing historical news data.

## Current Capabilities

The project can now perform the following:
*   **Historical News Fetching:** Utilizes the `gnews` library to fetch historical news article titles, publication dates, sources, and links. It fetches data month-by-month for a configurable query (defaulting to "world news") for the period from 2018 to 2024. (Note: Switched from `pygooglenews` to `gnews` for improved historical data fetching reliability and better dependency management).
*   **Sentiment Analysis:** Processes the fetched titles through the `SentimentAnalyzer` (using NLTK's VADER) to calculate a sentiment score for each.
*   **Data Storage:** Saves the fetched articles—including title, publication date (as datetime object), source, link, original published string, and the calculated sentiment score—into yearly Parquet files. These files are stored in the `fetched_news_data/` directory, with a naming convention of `news_YYYY.parquet` (e.g., `news_2018.parquet`).
*   **Data Aggregation:** Employs `pandas` to aggregate sentiment scores, calculating the average daily sentiment from the collected data.
*   **Visualization:** Generates two plots using `matplotlib` based on the entire fetched dataset (2018-2024):
    *   A plot of individual sentiment scores for each news title over time (`individual_sentiment_plot.png`).
    *   A plot of the aggregated average daily sentiment scores over time (`daily_average_sentiment_plot.png`).
    These plots are saved as PNG files in the root directory when the analysis script is run.

## How to Run

1.  **Install Dependencies:**
    Ensure you have Python 3.x installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `gnews`, `pandas`, `matplotlib`, `nltk`, and `pyarrow` (for Parquet support). NLTK's VADER lexicon will be downloaded on first use by the `SentimentAnalyzer` if not already present.

2.  **Run the Script:**
    Execute the main analysis script from the project root directory:
    ```bash
    python scripts/fetch_and_analyze.py
    ```
    This will initiate the process of fetching news data from 2018 to 2024, performing sentiment analysis, saving the data to yearly Parquet files in `fetched_news_data/`, and generating the sentiment trend plots. Be aware that fetching data for several years can take a significant amount of time.

## Future Goals

*   **Refined Data Acquisition:** Explore alternative news sources or APIs for more comprehensive and potentially richer datasets. Implement more robust error handling and rate limit management for API calls.
*   **Advanced Data Storage:** Evaluate and integrate more advanced database solutions (e.g., PostgreSQL, Elasticsearch) or data warehousing options for improved data management, querying capabilities, and scalability, especially as data volume grows.
*   **Deeper Temporal Analysis:** Enhance capabilities to group, aggregate, and analyze sentiment scores by more varied and customizable timeframes (e.g., specific events, quarterly trends).
*   **Advanced Sentiment & NLP:** Move beyond basic sentiment to explore more nuanced emotional analysis, topic modeling, or entity recognition within the news content.
*   **Interactive Visualization:** Develop interactive dashboards (e.g., using Dash/Plotly or Streamlit) to allow users to explore sentiment trends and filter data dynamically.
*   **Scalability and Performance:** Optimize the data processing pipeline for handling larger datasets and improve performance of fetching and analysis.
*   **Configuration:** Allow users to easily configure parameters like date ranges, news queries, and output directories via a configuration file or command-line arguments.

## Initial Tech Stack

*   **Programming Language:** Python
*   **Core NLP Library:** NLTK with VADER for sentiment analysis.
*   **News Fetching:** `gnews`
*   **Data Handling/Aggregation:** `pandas`
*   **Data Storage (Filesystem):** Parquet files (using `pyarrow`)
*   **Plotting:** `matplotlib`
*   **Testing:** Python's built-in `unittest` framework.

## Modularity and Design

The project will be developed with a strong emphasis on Object-Oriented Programming (OOP) principles to ensure modularity and maintainability. Key components such as data input, sentiment processing, data storage, and analysis will be designed as distinct modules or classes.

## Contribution Guidelines

(Placeholder for contribution guidelines - to be added later.)

## License

(Placeholder for license - likely MIT License, to be confirmed and added later.)
