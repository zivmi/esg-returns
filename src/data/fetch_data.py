# Import / install relevant Python packages
import pandas as pd     
import pandas_datareader as pdr
from pandas_datareader import wb 
import yfinance as yf
import wbdata
import datetime as dt
import matplotlib.pyplot as plt

# fetch data for all SP500 companies from 2010 to 2020 using yfinance 

def get_sp_data(start='2008-01-01', end=None):
    # Get the current SP components, and get a tickers list
    sp_assets = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    assets = sp_assets['Symbol'].str.replace('.', '-').tolist()
    # Download historical data to a multi-index DataFrame
    try:
        data = yf.download(assets, start=start, end=end, as_panel=False)
        filename = 'sp_components_data.pkl'
        data.to_pickle(filename)
        print('Data saved at {}'.format(filename))
    except ValueError:
        print('Failed download, try again.')
        data = None
    return data


if __name__ == '__main__':
    sp_data = get_sp_data()