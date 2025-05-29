import sys # Add sys import
import os # Add os import

# Add vendor directory to sys.path to use the vendored feedparser
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# VENDOR_DIR = os.path.join(SCRIPT_DIR, 'vendor')
# sys.path.insert(0, VENDOR_DIR) # Ensure this is commented out or removed

import datetime # Already here, but ensure it's available for gnews test
from datetime import date # Specifically import date for easy use
import calendar # For monthrange
import time # For sleep
# from pygooglenews import GoogleNews # No longer needed
from gnews import GNews # Use GNews
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

def fetch_news_gnews(query: str, start_date_tuple: tuple, end_date_tuple: tuple) -> list:
    """
    Fetches news articles using the gnews library for a given query and date range.
    """
    print(f"Fetching news using gnews for '{query}' from {start_date_tuple} to {end_date_tuple}...")
    gnews_client = GNews(language='en', country='US')
    gnews_client.start_date = start_date_tuple
    gnews_client.end_date = end_date_tuple
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

def plot_individual_sentiments(analyzed_df, filename="individual_sentiment.png"):
    """
    Plots individual sentiment scores over time.
    Assumes analyzed_df is a Pandas DataFrame with 'date_dt' and 'sentiment' columns.
    """
    if analyzed_df.empty:
        print("No data to plot for individual sentiments.")
        return

    print(f"Generating individual sentiment plot: {filename}...")
    plt.figure(figsize=(15, 7))
    
    # Sort by date just in case it's not already
    analyzed_df = analyzed_df.sort_values(by='date_dt')
    
    plt.plot(analyzed_df['date_dt'], analyzed_df['sentiment'], marker='o', linestyle='-', markersize=4, alpha=0.6)
    
    plt.title('Sentiment of Individual News Titles Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score (-1 to 1)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(minticks=10, maxticks=20)) # Adjust tick density
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Individual sentiment plot saved to {filename}")

def plot_aggregated_sentiments(aggregated_df, filename="aggregated_sentiment.png"):
    """
    Plots aggregated (e.g., daily average) sentiment scores over time.
    Assumes aggregated_df is a Pandas DataFrame with 'day' (or similar date column) 
    and 'average_sentiment' columns.
    """
    if aggregated_df.empty:
        print("No data to plot for aggregated sentiments.")
        return

    print(f"Generating aggregated sentiment plot: {filename}...")
    plt.figure(figsize=(15, 7))
    
    # Ensure 'day' is datetime for plotting if it's not already
    # If 'day' is already a date object (not datetime), matplotlib handles it well.
    # If it's a string, convert it: aggregated_df['day_dt'] = pd.to_datetime(aggregated_df['day'])
    # Let's assume 'day' column from groupby is already suitable (datetime.date objects)
    
    plt.plot(aggregated_df['day'], aggregated_df['average_sentiment'], marker='o', linestyle='-')
    
    plt.title('Average Daily Sentiment of News Titles Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score (-1 to 1)')
    plt.grid(True)
    plt.xticks(rotation=45)
    # Formatting for daily data
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(aggregated_df) // 20))) # Auto interval for days
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Aggregated sentiment plot saved to {filename}")

if __name__ == "__main__":
    # Removed the gnews test block and sys.exit()

    print("Starting news fetching and analysis process for 2018-2024 using gnews...")
    try:
        start_year = 2018
        end_year = 2024 # Inclusive
        news_query = "world news" 
        
        all_fetched_articles = [] 
        
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                # Create date tuples for gnews
                start_date_tuple = (year, month, 1)
                # Determine last day of the month
                last_day_val = calendar.monthrange(year, month)[1]
                end_date_tuple = (year, month, last_day_val)
                
                # Skip future months/years
                current_datetime = datetime.datetime.now() # Use datetime.datetime.now() for comparison
                if year > current_datetime.year or \
                   (year == current_datetime.year and month > current_datetime.month):
                    print(f"Skipping future period: {year}-{month:02d}")
                    if year > current_datetime.year: # If year is future, break from month loop to go to next year check or end
                        break 
                    continue # If current year but future month, continue to next month if any in current year

                # Call the new gnews fetching function
                # Note: The print message about date range is now inside fetch_news_gnews
                fetched_articles_for_month = fetch_news_gnews(
                    query=news_query, 
                    start_date_tuple=start_date_tuple, 
                    end_date_tuple=end_date_tuple
                )
                
                if fetched_articles_for_month: # fetch_news_gnews returns a list
                    all_fetched_articles.extend(fetched_articles_for_month)
                    print(f"Fetched {len(fetched_articles_for_month)} articles for {year}-{month:02d}. Total articles so far: {len(all_fetched_articles)}.")
                else:
                    print(f"No articles found for {year}-{month:02d}.")
                
                time.sleep(1) # Respectful delay

        print(f"\nFinished fetching all news. Total articles collected: {len(all_fetched_articles)}.")

        analyzed_articles_output = [] # Renamed to avoid confusion with original analyzed_articles
        if all_fetched_articles:
            # Initialize Sentiment Analyzer
            analyzer = SentimentAnalyzer()
            
            print("\nAnalyzing sentiment for all fetched articles...")
            for i, article in enumerate(all_fetched_articles):
                try:
                    sentiment_score = analyzer.analyze_sentiment(article['title'])
                    # Append all original article info along with sentiment
                    article_data_with_sentiment = article.copy() # Start with original article data
                    article_data_with_sentiment['sentiment'] = sentiment_score
                    analyzed_articles_output.append(article_data_with_sentiment)
                    
                    if (i + 1) % 50 == 0: # Print progress every 50 articles
                        print(f"Analyzed {i+1}/{len(all_fetched_articles)} articles...")
                except Exception as e:
                    print(f"Error analyzing article titled '{article.get('title', 'N/A')}': {e}")
            
            print(f"\nFinished sentiment analysis. Processed {len(analyzed_articles_output)} articles for sentiment.")
            
            if not analyzed_articles_output:
                print("No articles were successfully analyzed. Skipping data processing and plotting.")
            else:
                print("\nSample of analyzed articles (now includes sentiment):")
                for i, article_data in enumerate(analyzed_articles_output[:5]): # Print first 5
                    print(f" - Date: {article_data.get('date')}, Title: \"{article_data.get('title', 'N/A')[:50]}...\", Source: {article_data.get('source', 'N/A')}, Sentiment: {article_data.get('sentiment', float('nan')):.4f}")

                # Convert to Pandas DataFrame for easier manipulation
                # This df will contain all articles from 2018-2024 with their sentiment scores
                df = pd.DataFrame(analyzed_articles_output)

                aggregated_sentiments = None
                if not df.empty:
                    print("\nAggregating sentiment scores by day...")
                    # Ensure 'date' column is in datetime format (it should be from fetch_news_titles)
                    # If 'date' is already datetime objects, this is fine. If it's strings, conversion is needed.
                    # Assuming 'date' in analyzed_articles_output is already a datetime object from strptime.
                    df['date_dt'] = pd.to_datetime(df['date']) # Ensure it's pandas datetime for dt accessor
                    
                    # Extract just the date part for daily aggregation
                    df['day'] = df['date_dt'].dt.date 
                    
                    # Calculate average sentiment per day
                    daily_avg_sentiment = df.groupby('day')['sentiment'].mean().reset_index()
                    daily_avg_sentiment.rename(columns={'sentiment': 'average_sentiment'}, inplace=True)
                    
                    # Sort by date
                    daily_avg_sentiment.sort_values(by='day', inplace=True)
                    
                    aggregated_sentiments = daily_avg_sentiment
                    
                    print("\nSample of daily aggregated sentiment scores:")
                    print(aggregated_sentiments.head())

                    # --- Save data to yearly Parquet files ---
                    print("\nSaving data to yearly Parquet files...")
                    output_dir = "fetched_news_data"
                    os.makedirs(output_dir, exist_ok=True)

                    # df['date'] should already be datetime objects from fetch_news_titles
                    # pd.to_datetime might be redundant if 'date' is already datetime64[ns]
                    # but ensures it if 'date' was, for example, a list of mixed types or pure Python datetimes
                    df['date'] = pd.to_datetime(df['date'])

                    for year_to_save in range(start_year, end_year + 1):
                        # Filter for the current year. Using .copy() is good practice.
                        df_year = df[df['date'].dt.year == year_to_save].copy()
                        
                        if not df_year.empty:
                            file_path = os.path.join(output_dir, f"news_{year_to_save}.parquet")
                            try:
                                df_year.to_parquet(file_path, index=False)
                                print(f"Successfully saved {len(df_year)} articles for {year_to_save} to {file_path}")
                            except Exception as e:
                                print(f"Error saving Parquet file for {year_to_save}: {e}")
                        else:
                            print(f"No articles found for {year_to_save} to save.")
                    # --- End of saving data ---

                    # Call plotting functions
                    # Ensure plot_individual_sentiments uses the correct column if 'date_dt' is already datetime
                    # The function expects 'date_dt' and 'sentiment'
                    plot_individual_sentiments(df, filename="individual_sentiment_plot.png")
                    
                    if aggregated_sentiments is not None and not aggregated_sentiments.empty:
                         plot_aggregated_sentiments(aggregated_sentiments, filename="daily_average_sentiment_plot.png")
                    else: # This covers aggregated_sentiments being None or empty
                         print("Aggregated sentiment data was empty or None, skipping aggregated plot.")
                else: # This else corresponds to `if not df.empty` (after creating df from analyzed_articles_output)
                     print("DataFrame `df` (from analyzed_articles_output) is empty. No data to aggregate, save, or plot.")
        else: # This 'else' corresponds to 'if all_fetched_articles:'
            print("No articles were fetched for the entire period 2018-2024. Skipping analysis, saving, and plotting.")
        
        print("\nProcess complete.")
        if all_fetched_articles and analyzed_articles_output and not df.empty:
            print("Plots have been generated (if data was sufficient) and data saved.")
        else:
            print("No plots were generated and no data saved due to lack of data or issues in analysis/DataFrame creation.")

    except Exception as e:
        print(f"\nAn critical error occurred during the script execution: {e}")
        print("The process was halted due to this error.")
        # Optionally, re-raise the exception if you want to see the full traceback for debugging
        # raise 
