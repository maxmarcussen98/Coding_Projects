import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
import statsmodels
import pandas_datareader
from pandas_datareader import data as wb
import tkinter

#simple daily return plot
PG = wb.DataReader('PG', data_source='yahoo', start='1995-1-1') 
PG['simple_return'] = (PG['Adj Close']/PG['Adj Close'].shift(1))-1
PG['simple_return'].plot(figsize=(8, 5))
plt.show()

#calculating return of a few securities
tickers = ['PG', 'MSFT', 'F', 'GE']                                     
mydata = pd.DataFrame()                                                 
for t in tickers: 
    mydata[t] = wb.DataReader(t, data_source='yahoo', start='1995-1-1')['Adj Close'] 
(mydata / mydata.iloc[0]*100).plot(figsize = (15, 6))
plt.show()
#calculating return of a portfolio with same shares
returns = (mydata / mydata.shift(1)) - 1
weights = np.array([0.25, 0.25, 0.25, 0.25])
np.dot(returns, weights)
annual_returns = returns.mean() * 250
np.dot(annnual_returns, weights)

#calculating risk of a security
tickers = ['PG', 'BEI.DE']
sec_data = pd.DataFrame()
for t in tickers:
    sec_data[t] = wb.DataReader(t, data_source='yahoo', start='2007-1-1')['Adj Close']
sec_returns = np.log(sec_data / sec_data.shift(1)) #log returns
sec_returns['PG'].mean()*250 #annual rate of return
sec_returns['PG'].std() * 250 ** 0.5 #annual std. dev.

#calculating covariance between securities
# formula for covariance - rho = ((x-xbar)*(y-ybar))/(sigma x * sigma y)
# if cov is positive - two variables move in same direction
# if cov is negative - two variables move oppositely
# if cov is zero - two variables are independent
# correlation coefficient is the normalized version of covariance and tells us
    # more about strength of a linear relation
# covariance matrix - displays the covariance between two or more variables in a grid
    # (between 1 and 1, 1 and 2, 2 and 1, 2 and 2, etc.)

# calculating variances in python
PG_var = sec_returns['PG'].var()
BEI_var = sec_returns['BEI.DE'].var()
PG_var_a = sec_returns['PG'].var() * 250
BEI_var_a = sec_returns['BEI.DE'].var() * 250

#making covariance matrix - simple command
cov_matrix = sec_returns.cov()
cov_matrix_a = sec_returns.cov()*250

#making correlation matrix - also simple command
corr_matrix = sec_returns.corr() #gives correlation between returns
#we don't need to annualize this

#the risk of a portfolio is a function of the correlation between all of the
    #stocks that make it up!

# portfolio variance formula for 2 stocks: (w1sigma1+w1sigma2)^2 = w1^2sigma1^2+
    # 2w1sigma1w2sigma2rho1,2 +w2^2sigma2^2 - rho is correlation/covariance between
    # two (represent same thing)
    # w represents weights

#calculating portfolio risk in python
#Portfolio variance:
weights = np.array([0.5, 0.5])
pfolio_var = np.dot(weights.T, np.dot(sec_returns.cov()*250, weights))
#portfolio volatility
pfolio_vol = pfolio_var ** 0.5

#calculating diversifiable and non-diversifiable risk of a portfolio
weights = np.array([0.5, 0.5])
#diveersifiable risk:
PG_var_a = sec_returns['PG'].var() * 250
BEI_var_a = sec_returns['BEI.DE'].var() * 250
dr = pfolio_var - (weights[0] ** 2 * PG_var_a) -(weights[1] ** 2 * BEI_var_a)
print(str(round(dr*100, 3)) + '%')

n_dr_1 = pfolio_var - dr