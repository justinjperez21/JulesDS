import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import glob
from datetime import datetime

def generate_plot(df, date_col, value_col, title, filename, freq_formatter_major=None, freq_formatter_minor=None, is_scatter=False):
    """
    Helper function to generate and save a plot.
    """
    print(f"Generating plot: {title} -> {filename}...")
    plt.figure(figsize=(15, 7))
    
    if is_scatter:
        plt.plot(df[date_col], df[value_col], marker='o', linestyle='None', markersize=2, alpha=0.5)
    else:
        plt.plot(df[date_col], df[value_col], marker='o', linestyle='-', markersize=3)
        
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score")
    plt.grid(True)
    plt.xticks(rotation=45)
    
    ax = plt.gca()
    if freq_formatter_major:
        ax.xaxis.set_major_locator(freq_formatter_major['locator'])
        ax.xaxis.set_major_formatter(freq_formatter_major['formatter'])
    if freq_formatter_minor:
        ax.xaxis.set_minor_locator(freq_formatter_minor['locator'])

    plt.tight_layout()
    try:
        plt.savefig(filename)
        print(f"Successfully saved {filename}")
    except Exception as e:
        print(f"Error saving plot {filename}: {e}")
    plt.close()

def main():
    """
    Main function to load data, process, and generate plots.
    """
    print("Starting sentiment plotting process...")
    
    # Find CSV files
    data_dir = "data/"
    csv_pattern = os.path.join(data_dir, "news_*.csv")
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"No CSV files found in {data_dir} matching pattern {csv_pattern}. Exiting.")
        return
        
    print(f"Found {len(csv_files)} CSV files.")
    
    all_dataframes = []
    for f in csv_files:
        try:
            df = pd.read_csv(f)
            if not df.empty:
                all_dataframes.append(df)
            else:
                print(f"Warning: CSV file {f} is empty.")
        except Exception as e:
            print(f"Error reading CSV file {f}: {e}")
            
    if not all_dataframes:
        print("No data loaded from CSV files. Exiting.")
        return
        
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    if combined_df.empty:
        print("Combined DataFrame is empty after loading all files. Exiting.")
        return
        
    print(f"Successfully loaded and combined data. Total articles: {len(combined_df)}")

    # Data Cleaning/Preparation
    print("Cleaning and preparing data...")
    try:
        combined_df['date'] = pd.to_datetime(combined_df['date'])
    except Exception as e:
        print(f"Error converting 'date' column to datetime: {e}. Attempting with errors='coerce'.")
        combined_df['date'] = pd.to_datetime(combined_df['date'], errors='coerce')
        if combined_df['date'].isnull().any():
            print("Warning: Some dates could not be parsed and were set to NaT.")
            combined_df.dropna(subset=['date'], inplace=True) # Remove rows where date conversion failed

    if combined_df.empty:
        print("DataFrame is empty after date conversion and cleaning. Exiting.")
        return

    combined_df.sort_values(by='date', inplace=True)
    
    # --- Plot 1: Overall individual sentiment scores ---
    generate_plot(
        df=combined_df,
        date_col='date',
        value_col='sentiment',
        title='Overall Individual Article Sentiments (2018-2024)',
        filename='sentiment_overall_individual.png',
        freq_formatter_major={'locator': mdates.YearLocator(), 'formatter': mdates.DateFormatter('%Y')},
        freq_formatter_minor={'locator': mdates.MonthLocator()},
        is_scatter=True
    )

    # Sentiment Aggregation and Plotting
    # Set 'date' as index for resampling
    resample_df = combined_df.set_index('date')

    # --- Daily Aggregation ---
    print("Aggregating sentiment by day...")
    daily_sentiment = resample_df['sentiment'].resample('D').mean().reset_index()
    daily_sentiment.dropna(inplace=True) # Remove days with no data if any
    if not daily_sentiment.empty:
        generate_plot(
            df=daily_sentiment,
            date_col='date',
            value_col='sentiment',
            title='Daily Average Sentiment',
            filename='sentiment_daily.png',
            freq_formatter_major={'locator': mdates.YearLocator(), 'formatter': mdates.DateFormatter('%Y')},
            freq_formatter_minor={'locator': mdates.MonthLocator(bymonthday=1, interval=3)} # Quarterly ticks
        )
    else:
        print("No data for daily sentiment plot after aggregation.")

    # --- Weekly Aggregation ---
    print("Aggregating sentiment by week...")
    weekly_sentiment = resample_df['sentiment'].resample('W-MON').mean().reset_index() # Weekly, starting Monday
    weekly_sentiment.dropna(inplace=True)
    if not weekly_sentiment.empty:
        generate_plot(
            df=weekly_sentiment,
            date_col='date',
            value_col='sentiment',
            title='Weekly Average Sentiment',
            filename='sentiment_weekly.png',
            freq_formatter_major={'locator': mdates.YearLocator(), 'formatter': mdates.DateFormatter('%Y')},
            freq_formatter_minor={'locator': mdates.MonthLocator(bymonth=[1,4,7,10])} # Start of each quarter
        )
    else:
        print("No data for weekly sentiment plot after aggregation.")

    # --- Monthly Aggregation ---
    print("Aggregating sentiment by month...")
    monthly_sentiment = resample_df['sentiment'].resample('ME').mean().reset_index() # 'M' for month end
    monthly_sentiment.dropna(inplace=True)
    if not monthly_sentiment.empty:
        generate_plot(
            df=monthly_sentiment,
            date_col='date',
            value_col='sentiment',
            title='Monthly Average Sentiment',
            filename='sentiment_monthly.png',
            freq_formatter_major={'locator': mdates.YearLocator(), 'formatter': mdates.DateFormatter('%Y')},
            freq_formatter_minor={'locator': mdates.MonthLocator(interval=1)}
        )
    else:
        print("No data for monthly sentiment plot after aggregation.")

    # --- Yearly Aggregation ---
    print("Aggregating sentiment by year...")
    yearly_sentiment = resample_df['sentiment'].resample('YE').mean().reset_index() # 'Y' for year end
    yearly_sentiment.dropna(inplace=True)
    if not yearly_sentiment.empty:
        generate_plot(
            df=yearly_sentiment,
            date_col='date',
            value_col='sentiment',
            title='Yearly Average Sentiment',
            filename='sentiment_yearly.png',
            freq_formatter_major={'locator': mdates.YearLocator(), 'formatter': mdates.DateFormatter('%Y')}
        )
    else:
        print("No data for yearly sentiment plot after aggregation.")
        
    print("All plots generated.")

if __name__ == "__main__":
    main()
