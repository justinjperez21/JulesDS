import sys # Add sys import
import os # Add os import

# Add vendor directory to sys.path to use the vendored feedparser
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# VENDOR_DIR = os.path.join(SCRIPT_DIR, 'vendor')
# sys.path.insert(0, VENDOR_DIR) # Ensure this is commented out or removed

import datetime
# from datetime import date # No longer needed directly, use datetime.date
import argparse # For command-line arguments
# import calendar # No longer needed
import time
from gnews import GNews
import pandas as pd
# import matplotlib.pyplot as plt # Removed
# import matplotlib.dates as mdates # Removed
# We will also need SentimentAnalyzer

import sys # sys import is fine to keep
import os # os import is fine to keep
# Add the project root to sys.path to allow importing sentiment_analyzer
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # SCRIPT_DIR needed for PROJECT_ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..')) # Use SCRIPT_DIR
sys.path.insert(1, PROJECT_ROOT) # Insert after vendor dir (if vendor was active, now it's just general project root)
from sentiment_analyzer.analyzer import SentimentAnalyzer
# from datetime import datetime # Required for parsing date strings, already imported by `import datetime`

# Initialize GoogleNews client (Old - for pygooglenews) - REMOVED
# gn = GoogleNews(lang='en', country='US')

# Old fetch_news_titles function (pygooglenews-based) - REMOVED / REPLACED
# def fetch_news_titles(query: str, date_from: str, date_to: str): ...

def fetch_news_gnews(query: str, start_date_obj: datetime.date, end_date_obj: datetime.date) -> list:
    """
    Fetches news articles using the gnews library for a given query and date range.
    gnews expects start_date and end_date to be date objects.
    """
    print(f"Fetching news using gnews for '{query}' from {start_date_obj.strftime('%Y-%m-%d')} to {end_date_obj.strftime('%Y-%m-%d')}...")
    gnews_client = GNews(language='en', country='US')
    gnews_client.start_date = start_date_obj # Use date objects directly
    gnews_client.end_date = end_date_obj   # Use date objects directly
    gnews_client.max_results = 100  # Google News RSS typically limits to 100

    try:
        raw_articles = gnews_client.get_news(query)
    except Exception as e:
        print(f"Error calling gnews get_news for query '{query}': {e}")
        return []

    if not raw_articles:
        print("gnews returned no articles.")
        return []

    processed_articles = []
    articles_processed_count = 0
    for entry in raw_articles:
        title = entry.get('title')
        link = entry.get('url')
        published_date_str = entry.get('published date')
        publisher_dict = entry.get('publisher')
        source_name = publisher_dict.get('title') if isinstance(publisher_dict, dict) else None

        if title and published_date_str:
            try:
                # Example published_date_str: "Tue, 25 Jan 2022 08:00:00 GMT"
                date_obj = datetime.datetime.strptime(published_date_str, "%a, %d %b %Y %H:%M:%S %Z")
                processed_articles.append({
                    'title': title,
                    'date': date_obj,  # This is now a datetime object
                    'link': link,
                    'source': source_name,
                    'published_str': published_date_str # Keep original for reference
                })
                articles_processed_count +=1
            except ValueError as ve:
                print(f"Error parsing date '{published_date_str}' for article '{title}': {ve}. Skipping this article.")
            except Exception as e: # Catch any other unexpected error during processing an article
                print(f"An unexpected error occurred while processing article '{title}': {e}. Skipping this article.")
        else:
            # Log if essential fields are missing, but don't stop the loop
            missing_fields = []
            if not title: missing_fields.append("title")
            if not published_date_str: missing_fields.append("published_date")
            print(f"Skipping entry due to missing fields: {', '.join(missing_fields)}. Entry: {entry}")
            
    print(f"Successfully processed {articles_processed_count} articles out of {len(raw_articles)} raw results from gnews.")
    return processed_articles

# Removed plot_individual_sentiments function
# Removed plot_aggregated_sentiments function

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and analyze news sentiment for a given date range.")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format.")
    
    args = parser.parse_args()

    try:
        # Validate and parse dates from arguments
        start_date_dt_obj = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date_dt_obj = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        sys.exit(1)

    if start_date_dt_obj > end_date_dt_obj:
        print("Error: Start date cannot be after end date.")
        sys.exit(1)

    news_query = "world news"
    
    print(f"Starting news fetching and analysis for query '{news_query}' from {args.start_date} to {args.end_date}.")
    
    # Fetch news for the entire specified range
    all_fetched_articles = fetch_news_gnews(
        query=news_query,
        start_date_obj=start_date_dt_obj,
        end_date_obj=end_date_dt_obj
    )

    if not all_fetched_articles:
        print(f"No articles found for the period {args.start_date} to {args.end_date}. Exiting.")
        sys.exit(0) # Graceful exit as per requirement

    print(f"\nFetched {len(all_fetched_articles)} articles for the period {args.start_date} to {args.end_date}.")

    analyzed_articles_for_csv = [] 
    if all_fetched_articles:
        analyzer = SentimentAnalyzer()
        print(f"\nAnalyzing {len(all_fetched_articles)} articles...")
        for i, article in enumerate(all_fetched_articles):
            try:
                sentiment_score = analyzer.analyze_sentiment(article['title'])
                
                # Convert datetime object from gnews to 'YYYY-MM-DD HH:MM:SS' string for CSV
                date_str_formatted = article['date'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(article['date'], datetime.datetime) else str(article['date'])

                analyzed_articles_for_csv.append({
                    'title': article['title'],
                    'date': date_str_formatted, 
                    'link': article['link'],
                    'source': article['source'],
                    'sentiment': sentiment_score
                })
                if (i + 1) % 50 == 0 or (i + 1) == len(all_fetched_articles):
                    print(f"Analyzed {i+1}/{len(all_fetched_articles)} articles...")
            except Exception as e:
                print(f"Error analyzing article titled '{article.get('title', 'N/A')}': {e}")
        
        print(f"\nFinished sentiment analysis. Successfully processed {len(analyzed_articles_for_csv)} articles for sentiment.")

    if not analyzed_articles_for_csv:
        print("No articles were successfully analyzed or available after analysis. No CSV file will be created.")
        sys.exit(0) 

    # Save to CSV
    output_dir = "data/" 
    os.makedirs(output_dir, exist_ok=True)
    
    start_date_fn_str = start_date_dt_obj.strftime("%Y%m%d")
    end_date_fn_str = end_date_dt_obj.strftime("%Y%m%d")
    csv_filename = f"news_{start_date_fn_str}_{end_date_fn_str}.csv"
    csv_filepath = os.path.join(output_dir, csv_filename)

    print(f"\nSaving data to {csv_filepath}...")
    df_to_save = pd.DataFrame(analyzed_articles_for_csv)
    
    columns_to_save = ['title', 'date', 'link', 'source', 'sentiment']
    df_to_save = df_to_save[columns_to_save]
    
    try:
        df_to_save.to_csv(csv_filepath, index=False)
        print(f"Successfully saved {len(df_to_save)} analyzed articles to {csv_filepath}")
    except Exception as e:
        print(f"Error saving CSV file to '{csv_filepath}': {e}")

    print("\nProcess complete.")
