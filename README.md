# News Sentiment Analyzer

# Note: Overall thoughts(Human written)

Overall, Google Jules is an amazing tool. The model it uses(Gemini 2.5 Pro) is very capable and pleasant to work with. It makes good suggestions and is capable, moreso than other models in agent frameworks that I've used, at solving problems that arise on its own. It usually required minimal if any feedback/guidance from me, though this is a somewhat simple project so perhaps this does not hold true in larger, more complex codebases. The only problem I would cite is some issues with inconsistency in commiting to github and performance of the website. It was necessary sometimes to have it redo work purely because it was unable to commit to github. Since I worked on this it seems to be more consistent(as well as the daily task limit being raised from 5 to 60, which is extremely generous of Google). I very much like having this available on website, and I even used this from my phone in some cases while I did not have access to my computer, which opens up many opportunities. I very much enjoyed my time using Google Jules for this project, and I think I will use it in the future for other projects.

As for the project content, its very interesting to see that sentiment spikes during covid and only slowly falls. Of course, this could be for a variety of reasons(data sampling, sentiment scoring method, etc.). I would have thought the quarantine would have had such a large effect as to completely overwhelm these factors and still show a large negative trend, but I was wrong. NLTK vader also seems to have some interesting failure modes and tends to label a large amount of titles as completely neutral. I think 2 easy large improvements to this would be to get more data(ofcourse) and also use a more advanced sentiment analysis method, perhaps an LLM.

## Project Goal

This project aims to analyze sentiment in news articles over time to identify trends in the overall emotion of articles by year, month, week, etc., by fetching and processing historical news data.

## Project Structure

- `sentiment_analyzer/`: Contains the core sentiment analysis logic.
  - `analyzer.py`: Defines the `SentimentAnalyzer` class using NLTK's VADER.
- `scripts/`: Contains scripts for data processing.
  - `fetch_and_analyze.py`: Fetches news articles, performs sentiment analysis, and saves results to CSV files in the `data/` directory.
- `plot_sentiments.py`: Generates various sentiment trend plots from the data in `data/` and saves them as PNG files in the root directory.
- `data/`: Stores CSV files with fetched news data and sentiment scores. (This directory is ignored by git as specified in `.gitignore`)
- `tests/`: Contains unit tests for the project.
- `requirements.txt`: Lists project dependencies.
- `README.md`: This file, providing an overview of the project.
- `.gitignore`: Specifies intentionally untracked files that Git should ignore.

## Methodology

The project follows a multi-step process to analyze news sentiment:

1.  **Data Fetching**: The `scripts/fetch_and_analyze.py` script is used to gather news articles. It takes a start and end date as input and queries the GNews API for relevant articles within that timeframe. The script iterates monthly within the given range to ensure comprehensive data collection.
2.  **Sentiment Analysis**: For each fetched article, the title is processed by the `SentimentAnalyzer` class (located in `sentiment_analyzer/analyzer.py`). This analyzer uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner), a lexicon and rule-based sentiment analysis tool specifically attuned to sentiments expressed in social media, and generally well-suited for news headlines as well. It returns a compound sentiment score ranging from -1 (most negative) to +1 (most positive).
3.  **Data Storage**: The processed articles, including their titles, publication dates, sources, web links, and sentiment scores, are saved into CSV files. These files are stored in the `data/` directory, with filenames indicating the date range of the contained news (e.g., `news_20230101_20231231.csv`).
4.  **Data Visualization**: The `plot_sentiments.py` script reads all CSV files from the `data/` directory. It then aggregates the sentiment scores (calculating mean sentiment) across different timeframes: daily, weekly, monthly, and yearly. Using `matplotlib`, it generates line plots for these aggregated trends and a scatter plot for individual article sentiments over the entire period. These plots are saved as PNG images in the project's root directory (e.g., `sentiment_monthly.png`).

## Current Capabilities

The project performs the following:

*   **Historical News Fetching (`scripts/fetch_and_analyze.py`):**
    *   Utilizes the `gnews` library to fetch historical news articles (title, publication date, source, link).
    *   Accepts `start_date` and `end_date` command-line arguments to define the fetching period.
    *   To gather data over long periods (e.g., 2018-2024), it is run year-by-year. For example: `python scripts/fetch_and_analyze.py 2018-01-01 2018-12-31`, then `python scripts/fetch_and_analyze.py 2019-01-01 2019-12-31`, and so on, up to 2024.
    *   Performs sentiment analysis on fetched titles using `SentimentAnalyzer` (NLTK's VADER).
    *   Saves the processed data (including title, formatted date, link, source, and sentiment score) into CSV files.
    *   These CSV files are stored in the `data/` directory, with filenames like `news_STARTDATE_ENDDATE.csv` (e.g., `news_20220101_20221231.csv`).

*   **Sentiment Data Storage (`data/` directory):**
    *   This directory contains the CSV files generated by `scripts/fetch_and_analyze.py`, holding the raw article data and their sentiment scores.

*   **Sentiment Visualization (`plot_sentiments.py`):**
    *   Reads all CSV data from the `data/` directory.
    *   Aggregates sentiment scores (mean) daily, weekly, monthly, and yearly.
    *   Generates and saves the following plots as PNG files in the root directory:
        *   `sentiment_overall_individual.png`: A scatter plot showing the sentiment score of every individual news article over the entire date range. This helps visualize the distribution and density of sentiments.
        *   `sentiment_daily.png`: A line plot depicting the average sentiment score calculated on a daily basis. This plot helps identify short-term fluctuations.
        *   `sentiment_weekly.png`: A line plot showing the weekly average sentiment score, smoothing out daily variations and highlighting weekly trends.
        *   `sentiment_monthly.png`: A line plot of the monthly average sentiment, providing a clearer view of medium-term sentiment shifts.
        *   `sentiment_yearly.png`: A line plot illustrating the yearly average sentiment, useful for observing long-term trends and patterns.

## How to Run

1.  **Install Dependencies:**
    Ensure you have Python 3.x installed. Then, install the required packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    This installs `gnews`, `pandas`, `matplotlib`, and `nltk`. NLTK's VADER lexicon will be downloaded on first use by `SentimentAnalyzer` if not present.

2.  **Fetch News Data:**
    Run `scripts/fetch_and_analyze.py` for each year from 2018 to 2024 to populate the `data/` directory. Execute the command for each year individually:
    ```bash
    python scripts/fetch_and_analyze.py 2018-01-01 2018-12-31
    python scripts/fetch_and_analyze.py 2019-01-01 2019-12-31
    # ... and so on for 2020, 2021, 2022, 2023 ...
    python scripts/fetch_and_analyze.py 2024-01-01 2024-12-31
    ```
    Be mindful of potential API rate limits; the script includes a small delay, but running many fetches back-to-back might require additional pauses. Data will be saved in the `data/` directory.

3.  **Generate Sentiment Plots:**
    Once you have fetched the data, run `plot_sentiments.py` from the project root directory:
    ```bash
    python plot_sentiments.py
    ```
    This will read the CSV files from `data/` and generate the sentiment trend plots, saving them as PNG files in the root directory.

## Future Goals

*   **Refined Data Acquisition:** Explore alternative news sources or APIs for more comprehensive and potentially richer datasets. Implement more robust error handling and rate limit management for API calls.
*   **Advanced Data Storage:** Evaluate and integrate more advanced database solutions (e.g., PostgreSQL, Elasticsearch) or data warehousing options for improved data management, querying capabilities, and scalability, especially as data volume grows.
*   **Deeper Temporal Analysis:** Enhance capabilities to group, aggregate, and analyze sentiment scores by more varied and customizable timeframes (e.g., specific events, quarterly trends).
*   **Advanced Sentiment & NLP:** Move beyond basic sentiment to explore more nuanced emotional analysis, topic modeling, or entity recognition within the news content.
*   **Interactive Visualization:** Develop interactive dashboards (e.g., using Dash/Plotly or Streamlit) to allow users to explore sentiment trends and filter data dynamically.
*   **Scalability and Performance:** Optimize the data processing pipeline for handling larger datasets and improve performance of fetching and analysis.
*   **Configuration:** While `fetch_and_analyze.py` now accepts date arguments, further configuration options (e.g., news queries, output directories via a config file) could be explored.
