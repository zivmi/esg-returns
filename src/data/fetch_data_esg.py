import pandas as pd
import requests

# Downloads historic ESG ratings for a list of tickers and returns it as a single DataFrame
def get_combined_historic_esg():
    combined_esg_data = pd.DataFrame()
    
    # Fetch constituents of Nasdaq 100 from wikipedia
    constituents = pd.read_html(
        'https://en.wikipedia.org/wiki/Nasdaq-100')[4]
    
    tickers = constituents.Ticker.to_list()
    

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}

    for ticker in tickers:
        response = requests.get('https://query2.finance.yahoo.com/v1/finance/esgChart', params={"symbol": tickers},
                                headers=headers)

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

combined_esg_df = get_combined_historic_esg()

# Write data to CSV
combined_esg_df.to_csv("esg_data.csv")