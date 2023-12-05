import pandas as pd
from sqlalchemy import create_engine, Float, Date

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///data/financial_data.db')

# Read CSV files into pandas DataFrames
# Ensure dates are parsed correctly
esg_df = pd.read_csv('data/processed/esg_data_processed.csv', index_col=0, parse_dates=True)
fama_french_df = pd.read_csv('data/processed/fama_french_data_processed.csv', index_col=0, parse_dates=True )
monthly_returns_df = pd.read_csv('data/processed/monthly_returns_processed.csv', index_col=0, parse_dates=True)

# Preparing column data types for SQL
# Preparing column data types for SQL
esg_sql_types = {col: Float for col in esg_df.columns}
monthly_returns_sql_types = {col: Float for col in monthly_returns_df.columns}
fama_french_sql_types = {col: Float for col in esg_df.columns}

# Store DataFrames into SQLite database
esg_df.to_sql('esg_data', engine, if_exists='replace', dtype=esg_sql_types, index=True)
fama_french_df.to_sql('fama_french_data', engine, if_exists='replace', dtype=fama_french_sql_types, index=True)
monthly_returns_df.to_sql('monthly_returns', engine, if_exists='replace', dtype=monthly_returns_sql_types, index=True)

print("Data imported successfully into the SQLite database in the data folder.")
