import matplotlib.pyplot as plt
import csv
import numpy as np
import statistics as st
import math
import statsmodels.api as sm

olgaTime = []
mylaHere = []
examWeek = []
psetPages = []
psetPagesSquared = []
broTime = []

with open('schedule.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        if row[0] != "olgaTime":
            olgaTime.append(float(row[0]))
            mylaHere.append(float(row[1]))
            examWeek.append(float(row[2]))
            psetPages.append(float(row[3]))
            psetPagesSquared.append(float(row[3]) ** 2)
            broTime.append(float(row[4]))

y = olgaTime
x = [mylaHere, examWeek, psetPages, psetPagesSquared, broTime]

'''
I found some really sexy code online that uses statsmodels and 
gives me back all the data about the regression I might need!
'''

def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

print(reg_m(y, x).summary())

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x, y)

# display coefficients
print(regressor.coef_)
