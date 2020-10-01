import random
import numpy as np
import statistics as st
import statsmodels.api as sm
import csv
random.seed(1)

def calc_regression(x, y):
    var_array = np.cov(x, y)
    cov = var_array[0][1]
    x_var = var_array[0][0]
    y_var = var_array[1][1]
    b1 = cov/x_var
    b0 = np.mean(y)-b1*np.mean(x)
    print("b0 and b1:")
    print(b0, b1)
    return b0, b1


def random_data(num):
    xi1 = np.random.normal(1, 1.5, num)
    #print(st.stdev(xi1))
    xi2 = np.random.normal(1, 1.5, num)
    ui1 = []
    ei1 = []
    ui2 = []
    yi1 = []
    yi2 = []
    for xi in xi1:
        ui1.append(np.random.normal(0, abs(xi), 1)[0])
    ei = np.random.normal(0, 2, 50)
    for i in range(0, len(ei)):
        ui2.append(ei[i]+0.5*ui1[i])
    for i in range(0, len(xi1)):
        yi1.append(1-0.5*xi1[i]+ui1[i])
        yi2.append(1-0.5*xi2[i]+ui2[i])

    yi = []
    xi = []
    ui = []
    for i in range(0, len(yi1)):
        yi.append([yi1[i], yi2[i]])
        xi.append([xi1[i], xi2[i]])
        ui.append([ui1[i], ui2[i]])

    yi1 = np.array(yi1)
    yi2 = np.array(yi2)
    xi1 = np.array(xi1)
    xi1 = sm.add_constant(xi1, prepend=False)
    xi2 = np.array(xi2)
    xi2 = sm.add_constant(xi2, prepend=False)
    model1 = sm.OLS(yi1, xi1)
    result1 = model1.fit()
    print(result1.summary())
    model2 = sm.OLS(yi2, xi2)
    result2 = model2.fit()
    print(result2.summary())
    result1 = model1.fit(cov_type='HC0')
    print(result1.summary())
    result2 = model2.fit(cov_type='HC0')
    print(result2.summary())

    with open('pset4_dataset_50.csv', mode='w') as data_file:
        datawriter = csv.writer(data_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        for i in range(0, len(yi)):
            datawriter.writerow([yi[i], xi[i], ui[i]])

    return [yi, xi, ui]

random_data(50)