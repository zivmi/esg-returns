import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Float, Date
import statsmodels.api as sm
import matplotlib.pyplot as plt

## Create an SQLAlchemy engine
engine = create_engine('sqlite:///data/financial_data.db')

# SQL queries to select all data from each table
esg_query = "SELECT * FROM esg_data"
monthly_returns_query = "SELECT * FROM monthly_returns"
fama_french_query = "SELECT * FROM fama_french_data"

# Read the data into pandas DataFrames
esgdata = pd.read_sql(esg_query, engine).set_index('Date')
monthlyreturns = pd.read_sql(monthly_returns_query, engine).set_index('Date')
fama_french = pd.read_sql(fama_french_query, engine).set_index('Date')

# Convert index to datetime
esgdata.index = pd.to_datetime(esgdata.index, format='ISO8601')
monthlyreturns.index = pd.to_datetime(monthlyreturns.index, format='ISO8601')
fama_french.index = pd.to_datetime(fama_french.index, format='ISO8601')


# Prepare target variable
monthlyreturns = (monthlyreturns
    .loc[:'2019-11-01'] 
    .dropna(axis=1, how='all') # drop all columns with all NA values
)

intercept = (pd.DataFrame({"Intercept":np.repeat(1, len(esgdata[['Total_Score']]))})
    .set_index(esgdata.index)
)

# Join features
X = (esgdata[['Total_Score']]
    .join(fama_french)
    .drop(columns=["RF"])
    .join(intercept)
    .dropna()
    .loc[:'2019-11-01']
)

## FIT FAMA FRENCH 3 FACTOR MODEL

coefficients_3f = []
t_values_3f  = []

# Fit one linear model for each ticker in the monthlyreturns DataFrame
for col in monthlyreturns.columns:
    Y = monthlyreturns[col].to_frame()

    # Drop rows with NA values in the intersection of X and Y
    temp_df = Y.join(X).dropna()
    Y_temp = temp_df.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
    X_temp = temp_df.iloc[:, 2:].values.reshape(-1, 4) # ESG Score (Total_Score, column 1) is omitted 

    # Fit the model
    mod = sm.OLS(Y_temp, X_temp)
    res = mod.fit()

    coefficients_3f.append(list(res.params))
    t_values_3f.append(list(res.tvalues))
    
# Calculate averages
avg_coefficients_3f = np.mean(coefficients_3f, axis=0)
avg_t_values_3f  = pd.DataFrame(t_values_3f).mean(axis=0).to_numpy() #previous: np.mean(t_values, axis=0) does not work

# Format results
avg_coefficients_3f = pd.DataFrame(avg_coefficients_3f).T.rename(columns={0:"Mkt-RF", 1:"SMB", 2:"HML", 3:"Intercept"})
avg_coefficients_3f.index = ["Average Coefficients"]

avg_t_values_3f = pd.DataFrame(avg_t_values_3f).T.rename(columns={0:"Mkt-RF", 1:"SMB", 2:"HML", 3:"Intercept"})
avg_t_values_3f.index = ["Average t statistics"]

result_3f = pd.concat([avg_coefficients_3f, avg_t_values_3f])
result_3f.to_csv('reports/tables/3f_results.csv')
result_3f


# FIT 4 FACTOR MODEL (FF3 + ESG)

coefficients_4f = []
t_values_4f  = []

# Fit one linear model for each ticker in the monthlyreturns DataFrame
for col in monthlyreturns.columns:
    Y = monthlyreturns[col].to_frame()

    # Drop rows with NA values in the intersection of X and Y
    temp_df = Y.join(X).dropna()
    Y_temp = temp_df.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
    X_temp = temp_df.iloc[:, 1:].values.reshape(-1, 5)

    # Fit the model
    mod = sm.OLS(Y_temp, X_temp)
    res = mod.fit()

    coefficients_4f.append(list(res.params))
    t_values_4f.append(list(res.tvalues))
    
# Calculate averages
avg_coefficients_4f = np.mean(coefficients_4f, axis=0)
avg_t_values_4f = pd.DataFrame(t_values_4f).mean(axis=0).to_numpy() #previous: np.mean(t_values, axis=0) does not work

# Format results
avg_coefficients_4f = pd.DataFrame(avg_coefficients_4f).T.rename(columns={0:"Total_Score", 1:"Mkt-RF", 2:"SMB", 3:"HML", 4:"Intercept"})
avg_coefficients_4f.index = ["Average Coefficients"]

avg_t_values_4f = pd.DataFrame(avg_t_values_4f).T.rename(columns={0:"Total_Score", 1:"Mkt-RF", 2:"SMB", 3:"HML", 4:"Intercept"})
avg_t_values_4f.index = ["Average t statistics"]

result_4f = pd.concat([avg_coefficients_4f, avg_t_values_4f])
result_4f.to_csv('reports/tables/4f_results.csv')
result_4f

# Plot regression

df_temp = monthlyreturns.join(X).reset_index(drop=True)
df_plot = pd.melt(df_temp.iloc[:,:-4], id_vars=["Total_Score"]).dropna()

plt.figure(figsize=(10,6))
plt.scatter(df_plot["Total_Score"], df_plot["value"], alpha=0.5, s=10)
#plt.title('Monthly Returns vs. ESG Score')
plt.xlabel('ESG Score')
plt.ylabel('Returns [%]')

x = np.linspace(min(df_plot["Total_Score"])-0.5, max(df_plot["Total_Score"])+0.5, 100)
y = (avg_coefficients_4f.Intercept.values[0] + avg_coefficients_4f.Total_Score.values[0] * x)

plt.plot(x, y, color='red', linewidth=2, label='4-Factor model', alpha=0.5, linestyle='--')
plt.axhline(y=0.0, color='black', linewidth=0.2)
plt.legend()
plt.savefig('reports/figures/regression.png') # uncomment to save figure
