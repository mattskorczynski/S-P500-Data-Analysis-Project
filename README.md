# S-P500-Data-Analysis-Project
This repository contains Python code that scrapes historical stock price data for S&P 500 companies and performs analysis to calculate the Compound Annual Growth Rate (CAGR) of stock prices. The analysis focuses on the average stock price changes over the years from 2013 to 2022.

Overview

The code uses the Yahoo Finance API through the yfinance library to fetch historical stock price data for the S&P500.
It calculates the average stock price for each year within the specified date range using every closing date in the year.
The resulting data is saved to an Excel file.
The code also calculates the Stock Price CAGR (%) for each stock.
The analysis results are saved in separate sheets within the Excel file.

Prerequisites

Before running the code, make sure you have the following Python libraries installed:
yfinance: Used to fetch historical stock price data.
pandas: Used for data manipulation and analysis.
yahoo_fin: Used to fetch the list of S&P 500 tickers.
concurrent.futures: Used for parallel processing to improve runtime.
numpy: Required by pandas for numerical operations

Output

The Excel file contains the following sheets:
Raw Data: Raw stock price data for each S&P 500 stock.
CAGR Data: Calculated Stock Price CAGR (%) for each stock.
Top Stock Price CAGRs: Top 20 stocks with the highest Stock Price CAGR (%).
Middle Stock Price CAGRs: Middle 20 stocks with moderate Stock Price CAGR (%).
Bottom Stock Price CAGRs: Bottom 20 stocks with the lowest Stock Price CAGR (%).
