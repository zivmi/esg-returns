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
monthlyreturns = pd.read_csv(r'data/raw/monthly_returns.csv', index_col=0, parse_dates=True)

# Drop column with all NA
monthlyreturns = drop_columns_with_missing_values(monthlyreturns)

# Fill-Forward imputation
monthlyreturns = monthlyreturns.ffill()

# ESG and FF data are indexed by the first day of the month, 
# whereas monthly returns are indexed by the last day of the month, thus we shift returns by 1 day
monthlyreturns.index = monthlyreturns.index.shift(1, freq='D')

# Import ESG data
esgdata =  pd.read_csv(r'data/raw/esg_data.csv', index_col=1, parse_dates=True).drop(columns=['Unnamed: 0'])

agg_esgdata = esgdata.drop(columns=esgdata.columns)
for regex_word in ["Total_Score", "E_Score", "S_Score", "G_Score"]:
    temp_df = (esgdata
        .filter(regex=regex_word)
        .aggregate("max", axis="columns")
        .to_frame()
        .rename(columns={0:regex_word})
    )
    agg_esgdata.loc[:, regex_word] = temp_df.loc[:, regex_word]

# Fill Forward imputation
esgdata = agg_esgdata.ffill()#.loc[:'2019-11-01']

# Import FF data (does not need any processing)
famafrenchdata = pd.read_csv(r'data/raw/F-F_Research_Data_Factors.csv', index_col=1)
famafrenchdata.index = pd.to_datetime(famafrenchdata.index, format='%Y-%m-%d').rename('Date')
famafrenchdata = famafrenchdata.iloc[:, 1:] # drop unnamed column

# Specify the folder path
folder_path = 'data/processed/'

# Create the full path by joining the folder path and file name
output_path_mr = f'{folder_path}monthly_returns_processed.csv'
output_path_esg = f'{folder_path}esg_data_processed.csv'
output_path_ff = f'{folder_path}fama_french_data_processed.csv'

# Save to data processed folder
monthlyreturns.to_csv(output_path_mr, index=True)
esgdata.to_csv(output_path_esg, index=True)
famafrenchdata.to_csv(output_path_ff, index=True)