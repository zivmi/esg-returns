# Import / install relevant Python packages
import pandas as pd
import requests
import yfinance as yf
import os
from io import StringIO
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Define start and end data for data you want to fetch
# The timeseries will start the first of the month after the specified month. E.g. for 2014-08-01, the first data point will bi on 2014-09-01
# Note: after the return calculation the first row will be useless. E.g. we choose 2014-08-01 that our data then starts on 2014-10-01
start_date = '2014-08-01'
end_date = '2022-08-01'

# Fetch constituents of Nasdaq 100 from wikipedia
# If other Index is needed, exchange the link and the index of the table, e.g. for the S&P 500 use 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0] 
# and if name of column holding the tickers changed, must be updated in line 17 e.g. symbol for S&P 500
constituents = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[4]

# Create list from tickers
tickers = constituents.Ticker.to_list()


# Fetch csv file for Fama French factors from official website

def fetch_fama_french():

    # URL of the CSV file
    csv_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors.CSV"
    
    # Send a GET request to the URL
    response = requests.get(csv_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Read CSV starting from row 4 until row 1154
        df = pd.read_csv(StringIO(response.text), skiprows=3, nrows=1154)

        # Convert the 'Date' column to pandas datetime format
        df['Unnamed: 0'] = pd.to_datetime(df['Unnamed: 0'], format='%Y%m')

        # Convert the start_date string to a datetime object, add to month for reasons specified under the definition of the start date
        start_date_object = datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(months=2)

        # Format the datetime object to the desired format
        formatted_start_date = start_date_object.strftime("%Y%m") 

        # Specify the cutoff date
        cutoff_date = pd.to_datetime(formatted_start_date, format='%Y%m')

        # Filter rows based on the condition
        df = df[df['Unnamed: 0'] >= cutoff_date]

        return df
    else:
        return f"Failed to retrieve the file. Status code: {response.status_code}"
    
# Fetch montly returns for specific index

def fetch_monthly_returns(start_date, end_date, tickers):

    #display(tickers.head())

    try:
        # Fetch the stock prices for this tickers from yahoo finance
        prices = yf.download(tickers,start_date,end_date, auto_adjust=True)['Close']

        # Convert index to datetime so that 'resample' can be used
        prices.index = pd.to_datetime(prices.index)

        # Calculate the monthly returns
        monthly_returns = prices.resample('M').ffill().pct_change()

        # Drop first row as it is NA from return calculation
        monthly_returns = monthly_returns.iloc[1:]

    except ValueError:
        print('Failed download, try again.')
        prices = None

    return monthly_returns

# Downloads historic ESG ratings for a list of tickers and returns it as a single DataFrame
def fetch_esg(tickers):

    # Create dataframe to store data
    combined_esg_data = pd.DataFrame()
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}

    # Iterate over all tickers and send GET request
    for ticker in tickers:
        response = requests.get('https://query2.finance.yahoo.com/v1/finance/esgChart', params={"symbol": tickers},
                                headers=headers)

        # Create Dataframe from fetched data
        try:
            df = pd.DataFrame(response.json()["esgChart"]["result"][0]["symbolSeries"])
            df["Date"] = pd.to_datetime(df["timestamp"], unit="s")

            df = df.rename(columns={"esgScore": f"{ticker}_Total_Score",
                                    "environmentScore": f"{ticker}_E_Score",
                                    "socialScore": f"{ticker}_S_Score",
                                    "governanceScore": f"{ticker}_G_Score"})

            # Remove timestamp column
            df = df[['Date', f"{ticker}_Total_Score", f"{ticker}_E_Score", f"{ticker}_S_Score", f"{ticker}_G_Score"]]

            # Merge data for each ticker
            if combined_esg_data.empty:
                combined_esg_data = df
            else:
                combined_esg_data = pd.merge(combined_esg_data, df, on='Date', how='outer')

        except:
            print(f'An error has occurred for {ticker}. The ticker symbol might be wrong or you might need to wait to continue.')


    return combined_esg_data


# Specify the folder path
folder_path = 'data/raw/'

# Create the full path by joining the folder path and file name
output_path_mr = f'{folder_path}monthly_returns.csv'
output_path_esg = f'{folder_path}esg_data.csv'
output_path_ff = f'{folder_path}F-F_Research_Data_Factors.csv'

# Fetch data and save to folder data raw
fetch_monthly_returns(start_date,end_date,tickers).to_csv(output_path_mr, index=True)
fetch_esg(tickers).to_csv(output_path_esg, index=True)
fetch_fama_french().to_csv(output_path_ff, index=True)