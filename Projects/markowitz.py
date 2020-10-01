import numpy as np 
import pandas as pd 
from pandas_datareader import data as wb
import matplotlib.pyplot as plt 
'''
The Markowitz paper
Main lesson: investors shouldn't put all their eggs in one basket
-markowitz proved the existence of an "efficient frontier" of portfolios
    that maximized return for an amount of acceptable risk
-investments should be analyzed as part of a portfolio rather than one by one - 
    and financiers should understand how different securities in a portfolio
    interact with each other
we already know that combining securities with little correlation
    will minimize risk - markowitz also says that a diversified portfolio gives
    higher returns with no additional risk
markowitz assumes investors are rational and risk-averse
    for any level of risk, investors are most interested in 
    portfolio with higest returnip

given two stocks, there's an infinite number of combinations of weights (50-50, 
    60-40, 30-70) and one optimal one
-by graphing expected return vs. standard deviation, we get a sideways parabola looking
graph - there's a set of efficient portfolios that can provide the same or greater return
for the same risk
    -points below the curve are inefficient - can have a more profitable portfolio for same risk
    -points above the curve are impossible
'''

# getting the efficient frontier in python
# these are our inputs
assets = ['TRMT', 'SYNL', 'RFIL', 'RDCM', 'ORMP', 'OCC', 'MTR', 'JP', 'IDT', 'EDUC',
'CMCL', 'APEN', 'MDR', 'SRCI', 'FCAU', 'NCS', 'ATTO', 'GTE', 'BND', 'SWN']

start_date = '2016-1-1'

num_tests = 10
curr_equity = 6000

pf_data = pd.DataFrame()
print("Retrieving data...")
for a in assets:
    pf_data[a] = wb.DataReader(a, data_source = 'yahoo', start = start_date)['Adj Close']
(pf_data / pf_data.iloc[0] * 100).plot(figsize=(10, 5))

print("Data retrieved")

log_returns = np.log(pf_data / pf_data.shift(1))

num_assets = len(assets)
weights = np.random.random(num_assets)
weights /= np.sum(weights) #gives list of random weights that sum to one

# expected portfolio returns, variance, and volatility
returns = np.sum(weights * log_returns.mean())
variance = np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))
volatility = np.sqrt(variance)

# we're going to do 1000 combinations
pfolio_returns = []
pfolio_volatilities = []
pfolio_weights = []
curr_best = returns/volatility
best_returns = returns
best_vol = volatility
best_weights = weights

for x in range (num_tests):
    if x % 100 == 0:
        print("test " + str(x))
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    pfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
    pfolio_volatilities.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))
    pfolio_weights.append(weights)
    returns = (np.sum(weights*log_returns.mean())*250)
    volatility = (np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))
    ratio = returns/volatility
    if ratio > curr_best:
        curr_best = ratio
        best_weights = weights
        best_returns = returns
        best_vol = volatility
#turn this into a numpy array
pfolio_returns = np.array(pfolio_returns)
pfolio_volatilities = np.array(pfolio_volatilities)
weights_dict = {}
equity_dict = {}
for i in range(0, len(best_weights)):
    weights_dict[assets[i]] = best_weights[i]
    equity_dict[assets[i]] = best_weights[i] * curr_equity
print(str(num_tests) + " tests")
print("assets: " + str(assets))
print("weights:")
print(weights_dict)
print("Best return to risk ratio starting at " + start_date + ": " + str(curr_best))
print("Returns with this ratio: " + str(best_returns))
print("Volatility with this ratio: " + str(best_vol))
print("Equity to buy in each: ")
print(equity_dict)

portfolios = pd.DataFrame({'Return': pfolio_returns, 'Volatility': pfolio_volatilities, 'Weights': pfolio_weights})

portfolios.plot(x='Volatility', y='Return', kind='scatter', figsize=(10, 6))
plt.xlabel('Expected Volatility')
plt.ylabel('Expected Return')

plt.show()

