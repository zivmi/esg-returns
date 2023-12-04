import pandas as pd
from sqlalchemy import create_engine, Float, Date

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///data/financial_data.db')

# Read CSV files into pandas DataFrames
# Ensure dates are parsed correctly
esg_df = pd.read_csv('data/processed/esg_data_processed.csv')
fama_french_df = pd.read_csv('data/processed/fama_french_data_processed.csv', parse_dates=['Unnamed: 0'])
monthly_returns_df = pd.read_csv('data/processed/monthly_returns_processed.csv')

# Preparing column data types for SQL
esg_sql_types = {col: Float for col in esg_df.columns}
monthly_returns_sql_types = {col: Float for col in monthly_returns_df.columns}

# For Fama French data, date column is DATE type and others are FLOAT
# Here, 'Unnamed: 0' is assumed to be the name of your date column.
fama_french_sql_types = {'Unnamed: 0': Date, 'Mkt-RF': Float, 'SMB': Float, 'HML': Float, 'RF': Float}

# Store DataFrames into SQLite database
esg_df.to_sql('esg_data', engine, if_exists='replace', dtype=esg_sql_types, index=False)
fama_french_df.to_sql('fama_french_data', engine, if_exists='replace', dtype=fama_french_sql_types, index=False)
monthly_returns_df.to_sql('monthly_returns', engine, if_exists='replace', dtype=monthly_returns_sql_types, index=False)

print("Data imported successfully into the SQLite database in the data folder.")
