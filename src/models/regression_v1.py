# This tests if regressions work using our data
# Since the data sets are not 100% compatible yet, I modified them in Excel and imported them locally
# This needs to be adjusted once they are cleaned in SQL
####################################################

import pandas as pd
from sqlalchemy import create_engine

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///data/financial_data.db')

# SQL queries to select all data from each table
esg_query = "SELECT * FROM esg_data"
monthly_returns_query = "SELECT * FROM monthly_returns"

# Read the data into pandas DataFrames
esgdata = pd.read_sql(esg_query, engine)
monthlyreturns = pd.read_sql(monthly_returns_query, engine)

# Import monthly returns
# monthlyreturns = pd.read_csv(r'C:\Users\jenni\Desktop\extern_monthly_returns.csv')
# monthlyreturns = monthlyreturns.drop('Date', axis=1) # Drops date, not needed for regression
monthlyreturns = monthlyreturns.drop(['GEHC'], axis=1) # This is a column which only contains NaN

# Import changed ESG data
# esgdata =  pd.read_csv(r'C:\Users\jenni\Desktop\esg_data_change.csv')
# esgdata = esgdata.drop('Date', axis=1)

# Mean imputation
# monthlyreturns = monthlyreturns.fillna(monthlyreturns.mean())
# esgdata = esgdata.fillna(esgdata.mean())

# Regression specifications
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
regressor = LinearRegression() # Creates a LinearRegression Object

# Regression: Test without loop, not needed
#x = esgdata[['ADBE_E_Score', 'ADBE_G_Score']]
#y = monthlyreturns['ADI']
#regressor.fit(x,y)
#print('Intercept: \n', regressor.intercept_)
#print('Coefficients: \n', regressor.coef_)

# Regression using loop
x = esgdata[['ADBE_E_Score', 'ADBE_G_Score']]

intercepts = [] # Initialize lists to store intercepts and coefficients
coefficients = []

# Loop over each column in 'monthlyreturns'
for column in monthlyreturns.columns:
    # Get the column data as ‘y’
    y = monthlyreturns[column]
    # Fit the model
    regressor.fit(x,y)

    # Append the intercept and coefficients to the respective lists
    intercepts.append(regressor.intercept_)
    coefficients.append(regressor.coef_)

# Coefficients are stored in list of numpy arrays, converting to list of lists for readability
coefficients = [list(coef) for coef in coefficients]

# Print intercepts and coefficients
print('Intercepts: \n', intercepts)
print('Coefficients: \n', coefficients)