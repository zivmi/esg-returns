# fetch data from Fama-French data from http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html#BookEquity

import pandas as pd

# URL of the CSV file
csv_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors.CSV"

try:
    # Read the CSV file directly into a DataFrame, skipping the first three rows as they only contain information about the data set which is not needed.
    # If other data set is used that does not contain such information delete the 'skiprows=3'
    fama_french = pd.read_csv(csv_url, skiprows=3)

    # Display the DataFrame
    print(fama_french.head())

    # Save the DataFrame as a CSV file
    fama_french.to_csv('data/raw/F-F_Research_Data_Factors.CSV')

    # Catch errors
except pd.errors.ParserError as e:
    print(f"Error parsing CSV file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

