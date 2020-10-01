import matplotlib.pyplot as plt
import csv
import numpy as np
import statistics as st
import math

win = []
treat = []

with open('epoTests.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        if row[0] != "win":
            win.append(float(row[0]))
            treat.append(float(row[1]))

def get_tn():
    sum_treat = 0
    sum_not = 0
    sum_treat_win = 0
    sum_not_win = 0
    for i in range (0, len(win)):
        if treat[i] == 0:
            sum_not += 1
            if win[i] == 1:
                sum_not_win += 1
        else:
            sum_treat += 1
            if win[i] == 1:
                sum_treat_win += 1

    return (sum_treat_win/sum_treat) - (sum_not_win/sum_not)

def calc_regression():
    var_array = np.cov(treat, win)
    cov = var_array[0][1]
    treat_var = var_array[0][0]
    win_var = var_array[1][1]
    b1 = cov/treat_var
    b0 = np.mean(win)-b1*np.mean(treat)
    print("b0 and b1:")
    print(b0, b1)
    return b0, b1

def get_ssr(beta):
    ssr_sum = 0
    b0 = beta[0]
    b1 = beta[1]
    for i in range(0, len(treat)):
        win_conj = b0+b1*treat[i]
        ssr_sum += (win[i]-win_conj) ** 2
    return ssr_sum

print("Tn: " + str(get_tn()) + ", std. dev " + str(st.stdev(win)))
print(st.mean(win))
print(math.sqrt(get_ssr(calc_regression())))