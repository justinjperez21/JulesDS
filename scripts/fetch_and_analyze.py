import datetime
#from pygooglenews import GoogleNews
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# We will also need SentimentAnalyzer

import sys
import os
# Add the project root to sys.path to allow importing sentiment_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sentiment_analyzer.analyzer import SentimentAnalyzer

# Initialize GoogleNews client
# Using 'en' for English, 'US' for United States as a common default
# These can be parameterized later if needed.
#gn = GoogleNews(lang='en', country='US')

def fetch_news_titles(target_count=100): # target_count can be ignored or used to slice the sample
    print("Fetching news titles: Using PREDEFINED SAMPLE DATA.")
    sample_data = [
        {'title': 'Positive Outlook for Tech Stocks Next Quarter', 'date': datetime.datetime(2023, 10, 1, 10, 0, 0)},
        {'title': 'Global Markets Show Signs of Recovery', 'date': datetime.datetime(2023, 10, 1, 12, 30, 0)},
        {'title': 'New Environmental Policies Announced by Government', 'date': datetime.datetime(2023, 10, 2, 9, 15, 0)},
        {'title': 'Healthcare Reform Bill Faces Stiff Opposition', 'date': datetime.datetime(2023, 10, 2, 14, 0, 0)},
        {'title': 'Breakthrough in Cancer Research Reported by Scientists', 'date': datetime.datetime(2023, 10, 3, 11, 0, 0)},
        {'title': 'Dow Jones Hits Record High Amidst Economic Uncertainty', 'date': datetime.datetime(2023, 10, 3, 16, 45, 0)},
        {'title': 'Analysts Predict Volatile Week for Cryptocurrency', 'date': datetime.datetime(2023, 10, 4, 8, 30, 0)},
        {'title': 'Major Movie Studio Announces Sequel to Blockbuster Hit', 'date': datetime.datetime(2023, 10, 4, 13, 20, 0)},
        {'title': 'Ongoing Peace Talks Show Little Progress', 'date': datetime.datetime(2023, 10, 5, 10, 5, 0)},
        {'title': 'SpaceX Launches Another Successful Starlink Mission', 'date': datetime.datetime(2023, 10, 5, 18, 0, 0)},
        {'title': 'Debate Over New Education Curriculum Intensifies', 'date': datetime.datetime(2023, 10, 6, 9, 0, 0)},
        {'title': 'Tech Giant Unveils Next-Generation Smartphone', 'date': datetime.datetime(2023, 10, 6, 15, 30, 0)},
        {'title': 'Oil Prices Surge Following International Disputes', 'date': datetime.datetime(2023, 10, 7, 11, 10, 0)},
        {'title': 'Study Reveals Alarming Decline in Bee Populations', 'date': datetime.datetime(2023, 10, 7, 14, 40, 0)},
        {'title': 'Sports Team Secures Championship Title in Dramatic Finale', 'date': datetime.datetime(2023, 10, 8, 17, 0, 0)}
    ]
    # Return a slice of the data if target_count is smaller than the sample size
    return sample_data[:target_count]

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
        
        if analyzed_articles:
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
        else:
            if fetched_articles: # Only print this if we fetched articles but analysis failed for all
                 print("No articles were successfully analyzed to aggregate.")
    else: # This 'else' corresponds to 'if fetched_articles:'
        print("No articles fetched to analyze.")
    
    # Next steps (to be implemented in subsequent plan steps):
    # Aggregation is now done.
    print("\nProcess complete. Plots have been generated (if data was available).")
