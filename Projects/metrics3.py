import matplotlib.pyplot as plt
import csv
import numpy as np

y = []
x1 = []
x2 = []

with open('rSquared.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        if row[0] != "y":
            y.append(float(row[0]))
            x1.append(float(row[1]))
            x2.append(float(row[2]))
    print(len(x1))

def get_xy(xtype, ytype):
    if xtype=="x1":
        xlist = x1
    elif xtype=="x2":
        xlist = x2
    elif xtype=="y":
        xlist = y

    if ytype=="x1":
        ylist = x1
    elif ytype=="x2":
        ylist = x2
    elif ytype=="y":
        ylist = y

    return xlist, ylist

def show_scatter_plots():

    plt.scatter(x1,y)
    plt.title("x1")
    plt.show()

    plt.scatter(x2,y)
    plt.title("x2")
    plt.show()

def make_function(b0, b1, x):
    return b0+b1*x

def get_ssr(b0, b1, x, y):
    ssr_sum = 0
    for i in range(0, len(x)):
        y_conj = b0+b1*x[i]
        ssr_sum += (y[i]-y_conj) ** 2
    return ssr_sum


def plot_guess_line(b0, b1, xtype, ytype, xmax):
    x, y = get_xy(xtype, ytype)
    plt.scatter(x, y)
    print(get_ssr(b0, b1, x, y))
    plt.title(xtype+" with guess line")
    plt.plot([0, xmax], [b0, make_function(b0, b1, xmax)], 'k-')
    plt.show()

def calc_regression(xtype, ytype):
    x, y = get_xy(xtype, ytype)
    var_array = np.cov(x, y)
    cov = var_array[0][1]
    x_var = var_array[0][0]
    y_var = var_array[1][1]
    b1 = cov/x_var
    b0 = np.mean(y)-b1*np.mean(x)
    print("b0 and b1:")
    print(b0, b1)
    return b0, b1

def plot_regression(xtype, ytype):
    b0, b1 = calc_regression(xtype, ytype)
    plot_guess_line(b0, b1, xtype, ytype, 10)

def actual_reg(xtype, ytype):
    x, y = get_xy(xtype, ytype)
    results = {}

    coeffs = np.polyfit(x, y, 1)

     # Polynomial Coefficients
    results['coeffs'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['R2'] = ssreg / sstot

    return results

def show_residuals(xtype, ytype):
    coeffs = actual_reg(xtype, ytype)['coeffs']
    x2_residuals = []
    for i in range(0, len(x2)):
        residual = y[i] - (coeffs[0]*x2[i] + coeffs[1])
        x2_residuals.append(residual)
    plt.scatter(x2_residuals, x2)
    plt.show()
