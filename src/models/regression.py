# This tests if regressions work using our data
# Since the data sets are not 100% compatible yet, I modified them in Excel and imported them locally
# This needs to be adjusted once they are cleaned in SQL
####################################################

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine, Float, Date

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
esgdata.index = pd.to_datetime(esgdata.index, format='%Y-%m-%d')
monthlyreturns.index = pd.to_datetime(monthlyreturns.index, format='%Y-%m-%d')
fama_french.index = pd.to_datetime(fama_french.index, format='%Y-%m-%d')


regressor = LinearRegression() # Creates a LinearRegression Object

# Regression using loop
x = esgdata[['ADBE_E_Score']]

intercepts = [] # Initialize lists to store intercepts and coefficients
coefficients = []

# Loop over each column in 'monthlyreturns'
for column in monthlyreturns.columns:

    y = monthlyreturns[column]

    temp_df = x.join(y).dropna()

    x_temp = temp_df.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
    y_temp = temp_df.iloc[:, 1].values.reshape(-1, 1)  

    # Fit the model
    regressor.fit(x_temp, y_temp)

    # Append the intercept and coefficients to the respective lists
    intercepts.append(regressor.intercept_)
    coefficients.append(regressor.coef_)

# Coefficients are stored in list of numpy arrays, converting to list of lists for readability
coefficients = [list(coef) for coef in coefficients]
intercepts = [list(intercepts) for intercept in intercepts]

# Calculate averages
import numpy as np
avg_coef = np.mean(coefficients)
avg_int = np.mean(intercepts)
print(avg_coef)
print(avg_int)

# Plot
import matplotlib.pyplot as plt
x = np.linspace(-10, 10, 400)
y = avg_coef * x + avg_int

plt.figure(figsize=(10,6))
plt.plot(x, y)
plt.title('Regression of ABDE Score')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.savefig('reports/figures/regression.png') # uncomment to save figure
plt.show()

