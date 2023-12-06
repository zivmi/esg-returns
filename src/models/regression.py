import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine, Float, Date
import statsmodels.api as sm

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


regressor = LinearRegression() # Creates a LinearRegression Object

# NEW APPROACH:
import numpy as np
# Select the columns that end with 'T_Score'
#t_score_columns = [col for col in esgdata.columns if col.endswith('Total_Score')]
#X= np.mean(esgdata[t_score_columns]) # Not entirely correct
X=esgdata[['ADBE_Total_Score']]
#print(len(X)) # As test
#print(X) # As test

#Loop through each column and do regressions (example of simple linear regression with 'another_column' as independent variable):

intercepts = [] # Initialize lists to store intercepts and coefficients
coefficients = []

for col in monthlyreturns.columns:
    Y = monthlyreturns[col]

    temp_df = X.join(Y).join(fama_french).dropna()
    #print(temp_df) # To check

    Y_temp = temp_df.iloc[:, 1].values.reshape(-1, 1)  # values converts it into a numpy array
    #Y_temp = temp_df.iloc[:, 1:4].values.reshape(-1, 1)  
    X_temp = temp_df.iloc[:, [0, 2, 3, 4]].values.reshape(-1, 4)
    #print(X_temp) # To check 

# # Fit the model
    regressor.fit(X_temp, Y_temp)

# Append the intercept and coefficients to the respective lists
    intercepts.append(regressor.intercept_[0])
    coefficients.append(list(regressor.coef_[0]))

# coefficients = [list(coef) for coef in coefficients]
# intercepts = [list(intercepts) for intercept in intercepts]
#print(intercepts)

# Calculate averages
avg_coefficients = np.mean(coefficients, axis=0)
avg_intercept = np.mean(intercepts)
#print(avg_coefficients)
#print(avg_coefficients[1])
#print(temp_df)

# Plot
import matplotlib.pyplot as plt
x = np.linspace(-10, 10, 400)
y = avg_intercept + avg_coefficients[0] * esgdata[['ADBE_Total_Score']] + avg_coefficients[1] * temp_df[['Mkt-RF']] + avg_coefficients[2] * temp_df[['SMB']]  + avg_coefficients[3] * temp_df[['HML']] 


plt.figure(figsize=(10,6))
plt.plot(x, y)
plt.title('Regression of Total Score')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
# plt.savefig('reports/figures/regression.png') # uncomment to save figure
plt.show()

# Regression using loop
#x = esgdata[['ADBE_E_Score']]

#intercepts = [] # Initialize lists to store intercepts and coefficients
#coefficients = []

# Loop over each column in 'monthlyreturns'
# for column in monthlyreturns.columns:

#     y = monthlyreturns[column]

#     temp_df = x.join(y).dropna()

#     x_temp = temp_df.iloc[:, 0].values.reshape(-1, 1)  # values converts it into a numpy array
#     y_temp = temp_df.iloc[:, 1].values.reshape(-1, 1)  

#     # Fit the model
#     regressor.fit(x_temp, y_temp)

#     # Append the intercept and coefficients to the respective lists
#     intercepts.append(regressor.intercept_)
#     coefficients.append(regressor.coef_)

# # Coefficients are stored in list of numpy arrays, converting to list of lists for readability
# coefficients = [list(coef) for coef in coefficients]
# intercepts = [list(intercepts) for intercept in intercepts]

# # Calculate averages
# import numpy as np
# avg_coef = np.mean(coefficients)
# avg_int = np.mean(intercepts)
# print(avg_coef)
# print(avg_int)

# Plot
# import matplotlib.pyplot as plt
# x = np.linspace(-10, 10, 400)
# y = avg_coef * x + avg_int

# plt.figure(figsize=(10,6))
# plt.plot(x, y)
# plt.title('Regression of ABDE Score')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.grid(True)
# plt.savefig('reports/figures/regression.png') # uncomment to save figure
# plt.show()



