import matplotlib.pyplot as plt
import csv
import numpy as np
import statistics as st
import math
import statsmodels.api as sm

y = []
h = []
x1 = []
x2 = []
x3 = []
z = []
hhat = []

with open('soundcloud.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        if row[0] != "y":
            y.append(float(row[0]))
            h.append(float(row[1]))
            x1.append(float(row[2]))
            x2.append(float(row[3]))
            x3.append(float(row[4]))
            z.append(float(row[5]))
            hhat.append((-9.4914 * float(row[5]) + 22.3623))

print(len(hhat))
print(len(z))
print(len(y))

x = [hhat, x1, x2, x3]

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
#print(sm.OLS(y, x).fit().summary())