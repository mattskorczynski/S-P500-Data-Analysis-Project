import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
import concurrent.futures

# Ignore SSL certificate verification
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Function to fetch data for a symbol and split into 1-year intervals
def scrape_data(symbol):
    try:
        # Download historical stock data from 2013 to 2022 using yfinance
        stock = yf.Ticker(symbol)
        hist_data = stock.history(start="2013-01-01", end="2022-12-31")

        # Check if the data is within the desired time range
        if hist_data.empty:
            return None

        # Create a list of DataFrames to store results for each year
        year_results = []

        for year in range(2013, 2023):
            # Filter data for each year
            year_data = hist_data[hist_data.index.year == year]

            if year_data.empty:
                continue

            # Calculate average stock price for the year
            avg_stock_price = round(year_data['Close'].mean(), 4)

            # Determine the year for the first row
            year_label = year_data.index[0].year

            # Create a DataFrame for the current year's results
            year_result = pd.DataFrame({
                'Year': [year_label],
                'Average Stock Price ($)': [avg_stock_price],
                'Symbol': [symbol]
            })

            year_results.append(year_result)

        return year_results

    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return None

# Get the list of S&P 500 stocks
sp500 = si.tickers_sp500()

# List of DataFrames to store results for all stocks
final_results = []

# concurrent.futures for parallel processing to make run time faster
with concurrent.futures.ThreadPoolExecutor() as executor:
    for symbol_results in executor.map(scrape_data, sp500):
        if symbol_results is not None:
            final_results.extend(symbol_results)

# Concatenate all results into a single DataFrame
final_df = pd.concat(final_results, ignore_index=True)

# Create an Excel file with the results
with pd.ExcelWriter('sp500_StockPrice_CAGR_data_analysis.xlsx', engine='openpyxl') as writer:
    final_df.to_excel(writer, sheet_name='Raw Data', index=False)

    # Calculate stock price CAGR for each stock
    cagr_results = []
    for symbol in sp500:
        stock_data = final_df[final_df['Symbol'] == symbol]
        if not stock_data.empty:
            num_intervals = len(stock_data) - 1
            if num_intervals > 0:  # Avoid division by zero
                stock_price_cagr = (
                    (stock_data.iloc[-1]['Average Stock Price ($)'] / stock_data.iloc[0]['Average Stock Price ($)']) ** (1 / num_intervals) - 1
                )
            else:
                stock_price_cagr = 0.0  # Set to 0 if no intervals

            cagr_result = pd.DataFrame({
                'Symbol': [symbol],
                'Stock Price CAGR (%)': [stock_price_cagr * 100],
            })
            cagr_results.append(cagr_result)

    cagr_df = pd.concat(cagr_results, ignore_index=True)
    cagr_df.to_excel(writer, sheet_name='CAGR Data', index=False)

    # Sort the CAGR data in descending order
    sorted_cagr_df = cagr_df.sort_values(by='Stock Price CAGR (%)', ascending=False)

    # Split the sorted data into top 20, middle, and bottom categories
    top_stock_price_cagr = sorted_cagr_df.head(20)
    middle_stock_price_cagr = sorted_cagr_df.iloc[len(sorted_cagr_df) // 2 - 10:len(sorted_cagr_df) // 2 + 10]
    bottom_stock_price_cagr = sorted_cagr_df.tail(20)

    # Write the top 20 Stock Price CAGRs to the Top Stock Price CAGRs sheet
    top_stock_price_cagr.to_excel(writer, sheet_name='Top Stock Price CAGRs', index=False)

    # Write the middle 20 Stock Price CAGRs to the Middle Stock Price CAGRs sheet
    middle_stock_price_cagr.to_excel(writer, sheet_name='Middle Stock Price CAGRs', index=False)

    # Write the bottom 20 Stock Price CAGRs to the Bottom Stock Price CAGRs sheet
    bottom_stock_price_cagr.to_excel(writer, sheet_name='Bottom Stock Price CAGRs', index=False)

print("Data saved to sp500_StockPrice_CAGR_data_analysis.xlsx")
