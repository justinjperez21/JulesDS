import sys # Add sys import
import os # Add os import

# Add vendor directory to sys.path to use the vendored feedparser
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_DIR = os.path.join(SCRIPT_DIR, 'vendor')
sys.path.insert(0, VENDOR_DIR)

import datetime
from pygooglenews import GoogleNews
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# We will also need SentimentAnalyzer

import sys
import os
# Add the project root to sys.path to allow importing sentiment_analyzer
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..')) # Use SCRIPT_DIR
sys.path.insert(1, PROJECT_ROOT) # Insert after vendor dir
from sentiment_analyzer.analyzer import SentimentAnalyzer
from datetime import datetime # Required for parsing date strings

# Initialize GoogleNews client
# Using 'en' for English, 'US' for United States as a common default
# These can be parameterized later if needed.
gn = GoogleNews(lang='en', country='US')

def fetch_news_titles(target_count=100):
    print("Fetching news titles using pygooglenews for 'world news' in the last 7 days...")
    try:
        search_results = gn.search('world news', when='7d')
    except Exception as e:
        print(f"Error calling pygooglenews search: {e}")
        return []

    if not search_results or 'entries' not in search_results or not search_results['entries']:
        print("No news entries found by pygooglenews search.")
        return []

    articles = []
    for entry in search_results['entries']:
        if len(articles) >= target_count:
            break # Stop if we have reached the target count
        
        title = entry.get('title')
        published_date_str = entry.get('published')
        
        if title and published_date_str:
            try:
                # Example published_date_str: "Mon, 16 Oct 2023 10:00:00 GMT"
                # This format is directly parseable by strptime with %a, %d %b %Y %H:%M:%S %Z
                date_obj = datetime.strptime(published_date_str, "%a, %d %b %Y %H:%M:%S %Z")
                articles.append({'title': title, 'date': date_obj})
            except ValueError as ve:
                print(f"Error parsing date '{published_date_str}' for article '{title}': {ve}. Skipping this article.")
            except Exception as e:
                print(f"An unexpected error occurred while processing article '{title}': {e}. Skipping this article.")
        else:
            print(f"Missing title or published date for an entry. Entry: {entry}")
            
    if not articles:
        print("No articles could be processed, even if entries were found.")
    else:
        print(f"Successfully fetched and processed {len(articles)} articles.")
        
    return articles

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
    print("Starting news fetching and analysis process...")
    try:
        # Fetch news (aiming for 100 articles for now)
        # We'll increase this to 1000 later as requested by the user.
        fetched_articles = fetch_news_titles(target_count=1000)
        
        analyzed_articles = []
        if fetched_articles:
            print(f"\nSuccessfully fetched {len(fetched_articles)} articles.")
            
            # Initialize Sentiment Analyzer
            analyzer = SentimentAnalyzer()
            
            print("\nAnalyzing sentiment for fetched articles...")
            for i, article in enumerate(fetched_articles):
                try:
                    sentiment_score = analyzer.analyze_sentiment(article['title'])
                    analyzed_articles.append({
                        'date': article['date'],
                        'title': article['title'],
                        'sentiment': sentiment_score
                    })
                    if (i + 1) % 10 == 0: # Print progress every 10 articles
                        print(f"Analyzed {i+1}/{len(fetched_articles)} articles...")
                except Exception as e:
                    print(f"Error analyzing article '{article['title']}': {e}")
            
            print(f"\nFinished sentiment analysis. Processed {len(analyzed_articles)} articles.")
            
            if not analyzed_articles:
                print("No articles were successfully analyzed. Skipping data processing and plotting.")
            else:
                print("\nSample of analyzed articles:")
                for i, article_data in enumerate(analyzed_articles[:5]): # Print first 5
                    print(f" - Date: {article_data['date']}, Title: \"{article_data['title'][:50]}...\", Sentiment: {article_data['sentiment']:.4f}")

                # Convert to Pandas DataFrame for easier manipulation
                df = pd.DataFrame(analyzed_articles)

                aggregated_sentiments = None
                if not df.empty:
                    print("\nAggregating sentiment scores by day...")
                    # Ensure 'date' column is in datetime format
                    df['date_dt'] = pd.to_datetime(df['date'])
                    
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

                    # Call plotting functions
                    if not df.empty: # df contains individual analyzed articles
                         plot_individual_sentiments(df, filename="individual_sentiment_plot.png")
                    
                    if aggregated_sentiments is not None and not aggregated_sentiments.empty:
                         plot_aggregated_sentiments(aggregated_sentiments, filename="daily_average_sentiment_plot.png")
                    elif not df.empty : # If aggregation resulted in empty but individual data was there
                         print("Aggregated sentiment data was empty, skipping aggregated plot.")
                else: # This else corresponds to `if not df.empty` which implicitly means analyzed_articles was not empty but df creation failed or df is empty.
                     print("DataFrame could not be created or is empty. No data to aggregate or plot.")
        else: # This 'else' corresponds to 'if fetched_articles:'
            print("No articles were fetched. Skipping analysis and plotting.")
        
        print("\nProcess complete.")
        if fetched_articles and analyzed_articles:
            print("Plots have been generated (if data was sufficient).")
        else:
            print("No plots were generated due to lack of data.")

    except Exception as e:
        print(f"\nAn unexpected error occurred during the script execution: {e}")
        print("The process was halted due to this error.")
        # Optionally, re-raise the exception if you want to see the full traceback for debugging
        # raise 
