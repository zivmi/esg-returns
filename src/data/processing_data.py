# This script cleans the data that it can be used in the regression

import pandas as pd

# Drop columns with all missing values
def drop_columns_with_missing_values(df):
    cols_before = df.columns
    df = df.dropna(axis=1, how='all')
    cols_after = df.columns
    dropped_cols = set(cols_before) - set(cols_after)
    print(f"Columns dropped due to all missing values: {dropped_cols}")

    return df

# Import monthly returns
monthlyreturns = pd.read_csv(r'data/raw/monthly_returns.csv')
# Drop column with all NA
drop_columns_with_missing_values(monthlyreturns)


# Import ESG data
esgdata =  pd.read_csv(r'data/raw/esg_data.csv')
# Drop Date column as it is not needed for regression
esgdata = esgdata.drop('Date', axis=1)

# Remove first row as time window from return calculation in monthly returns changed by one month
esgdata = esgdata.iloc[1:]


# Mean imputation: fill missing values with the mean
monthlyreturns = monthlyreturns.fillna(monthlyreturns.mean())
esgdata = esgdata.fillna(esgdata.mean())

# Import ESG data (does not need any processing)
famafrenchdata =  pd.read_csv(r'data/raw/F-F_Research_Data_Factors.csv')

# Specify the folder path
folder_path = 'data/processed/'

# Create the full path by joining the folder path and file name
output_path_mr = f'{folder_path}monthly_returns_processed.csv'
output_path_esg = f'{folder_path}esg_data_processed.csv'
output_path_ff = f'{folder_path}fama_french_data_processed.csv'

# Save to data processed folder
monthlyreturns.to_csv(output_path_mr, index=False)
esgdata.to_csv(output_path_esg, index=False)
famafrenchdata.to_csv(output_path_ff, index=False)