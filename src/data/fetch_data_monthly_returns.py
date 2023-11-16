# Import packages
import yfinance as yf
import pandas as pd

def fetch_monthly_returns(start_date, end_date):

    # Fetch constituents of Nasdaq 100 from wikipedia
    constituents = pd.read_html(
        'https://en.wikipedia.org/wiki/Nasdaq-100')[4]

    #display(tickers.head())

    # Fetch the stock prices for this tickers from yahoo finance
    prices = yf.download(constituents.Ticker.to_list(),start_date,end_date, auto_adjust=True)['Close']

    # Calculate the monthly returns
    monthly_returns = prices.resample('M').ffill().pct_change()

    # Drop first row as it is NA from return calculation
    monthly_returns = monthly_returns.iloc[1:]

    return monthly_returns

start_date = '2014-08-01'
end_date = '2022-08-01'

m_returns = fetch_monthly_returns(start_date, end_date)

# Write to csv
m_returns.to_csv('monthly_returns.csv')