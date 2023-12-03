import pandas as pd
from sqlalchemy import create_engine, Float, Date

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///data/financial_data.db')

# Read CSV files into pandas DataFrames
esg_df = pd.read_csv('data/processed/esg_data_processed.csv')
fama_french_df = pd.read_csv('data/processed/fama_french_data_processed.csv')
monthly_returns_df = pd.read_csv('data/processed/monthly_returns_processed.csv')

# Preparing column data types for SQL
# Assuming all columns in ESG and Monthly Returns data are floats
esg_sql_types = {col: Float for col in esg_df.columns}
monthly_returns_sql_types = {col: Float for col in monthly_returns_df.columns}

# For Fama French data, date column is DATE type and others are FLOAT
fama_french_sql_types = {col: Date if col == 'Unnamed: 0' else Float for col in fama_french_df.columns}

# Store DataFrames into SQLite database
esg_df.to_sql('esg_data', engine, if_exists='append', dtype=esg_sql_types, index=False)
fama_french_df.to_sql('fama_french_data', engine, if_exists='append', dtype=fama_french_sql_types, index=False)
monthly_returns_df.to_sql('monthly_returns', engine, if_exists='append', dtype=monthly_returns_sql_types, index=False)

print("Data imported successfully into the SQLite database in the data folder.")
