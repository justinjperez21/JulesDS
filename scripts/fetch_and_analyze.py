import datetime
from pygooglenews import GoogleNews
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
gn = GoogleNews(lang='en', country='US')

def fetch_news_titles(target_count=1000): # Aim for 1000 articles
    """
    Fetches recent news titles and their publication dates using pygooglenews.
    Aims to get close to target_count recent articles.
    Google News RSS typically returns about 100 articles per query.
    We might need to use broader timeframes or multiple queries for more.
    For now, let's fetch news from the last few days.
    """
    print(f"Fetching recent news titles (aiming for up to {target_count} articles)...")
    
    # Search for general news over the last 7 days
    # The 'when' parameter is crucial. '7d' means last 7 days.
    # Using a generic search like "news" or relying on top_news might be an option.
    # Let's try top_news first, then search if needed.
    
    all_entries = []
    
    try:
        # top_news() usually gives the most recent general news
        top = gn.top_news(proxies=None, scraping_bee=None) # No proxy, no scrapingbee
        if top and 'entries' in top:
            all_entries.extend(top['entries'])
            print(f"Fetched {len(top['entries'])} entries from top_news.")

        # To get more entries, we can try searching for broad terms over a period.
        # Google News search results are typically limited to around 100 per query.
        # If we need more, we'd have to get creative with search terms or time windows.
        # For now, let's assume top_news() gives a good set of recent articles.
        # If len(all_entries) < target_count:
        #     search_results = gn.search("news", when="7d") # Example broad search
        #     if search_results and 'entries' in search_results:
        #         all_entries.extend(search_results['entries'])
        #     # Need to de-duplicate if combining sources

        # Extract title and published date
        news_items = []
        seen_titles = set()

        for entry in all_entries:
            title = getattr(entry, 'title', None)
            # feedparser can have 'published_parsed' or 'updated_parsed'
            # 'published_parsed' is usually what we want for original publication
            pub_time_struct = getattr(entry, 'published_parsed', None)
            
            if title and title not in seen_titles and pub_time_struct:
                # Convert time.struct_time to datetime object
                publication_date = datetime.datetime(*pub_time_struct[:6])
                news_items.append({'date': publication_date, 'title': title})
                seen_titles.add(title)
        
        # Sort by date in descending order (most recent first)
        news_items.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"Processed {len(news_items)} unique news items with dates.")
        return news_items[:target_count] # Return up to the target count

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

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
