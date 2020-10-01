import numpy as np
import statistics as st
import statsmodels.api as sm
import csv
from linearmodels.iv import IV2SLS
import pandas as pd

Q = np.random.normal(0, 1, 100)
R = np.random.normal(0, 1, 100)
V = np.random.normal(0, 1, 100)
W = np.random.normal(0, 1, 100)
U = []
Xreal = []
Z = []
Y = []
Xhat = []
for i in range(0, len(R)):
    U.append(V[i]+R[i])
    Xreal.append(0.2+W[i]+2*V[i])
    Z.append(-0.5+W[i]+Q[i])
    Y.append(0.2+0.3*Xreal
    	[i]+U[i])
    Xhat.append(0.3+Z[i]-Q[i]+2*V[i])

x = [Xhat]

# 1.2.2
def reg_m(y, x):
    ones = np.ones(len(x[0]))
    X = sm.add_constant(np.column_stack((x[0], ones)))
    for ele in x[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(y, X).fit()
    return results

print(reg_m(Y, x).summary())

# 1.2.2
with open('pset4_dataset_100.csv', mode='w') as data_file:
    datawriter = csv.writer(data_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    for i in range(0, len(Y)):
        datawriter.writerow([Q[i], R[i], V[i], W[i], U[i], Xreal[i], Z[i], Y[i]])
