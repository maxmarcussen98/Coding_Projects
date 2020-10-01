# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 21:07:27 2019

@author: maxma
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels as sm
from statsmodels.discrete.discrete_model import Probit

class FertilitySim:
    
    def __init__(self, params, num_ind=100000):
        
        
        
        self.NumInd = num_ind
        self.DataColumns = ['X', 't', 'u', 'epsilon', 'xi', 'W', 'beta', 'f', 'K', 'H']
        
        '''
        parameters: eta, a, gamma, delta, delta0, rho
        '''
        
        self.eta = params['eta']
        self.a = params['a']
        self.gamma = params['gamma']
        self.delta = params['delta']
        self.delta0 = params['delta0']
        self.rho = params['rho']
        
        self.RawData = pd.DataFrame(columns=self.DataColumns)
        
    def simulate(self):
        '''
        Simulates data. Should be clear which line is doing which variable.
        '''
        np.random.seed(1234)
        
        #x is used to generate wagesdat
        self.RawData['X'] = np.random.normal(0, 1, self.NumInd)
        #t is exogenous wage from having a kid - utility of having a child
        self.RawData['t'] = np.random.normal(0, 1, self.NumInd)
        #randoms
        self.RawData['u'] = np.random.normal(0, 1, self.NumInd)
        self.RawData['epsilon'] = np.random.normal(0, 1, self.NumInd)
        self.RawData['xi'] = np.random.normal(0, 1, self.NumInd)
        #log wages
        self.RawData['W'] = (self.eta * self.RawData['X'] + self.RawData['t'] + self.RawData['u']).clip(lower=0)
        self.RawData['W'] = self.RawData['W'].clip(lower=0)
        #log beta
        self.RawData['beta'] = self.RawData['X'] + self.RawData['epsilon'] + self.a * self.RawData['xi']
        #fertility choice
        self.RawData['f'] = np.random.choice(2, self.NumInd)
        #log wages with a child
        self.RawData['K'] = (self.RawData['W'] + \
        + self.delta * self.RawData['t'] + self.RawData['xi'] + self.delta0)

        #hours
        self.RawData['H'] =  (((1-self.RawData['f']) * self.rho * np.exp(self.RawData['W']) + \
        self.RawData['f'] * self.rho * np.exp(self.RawData['K']) * self.RawData['t']) \
        / np.exp(self.RawData['beta'])) 
        self.RawData['H'] = self.RawData['H'].clip(lower=0)
        self.RawData['H'] = self.RawData['H'] ** (1/self.gamma)
        self.RawData['H'] = self.RawData['H'].clip(upper=100)
        
        
def probitfn(dataset):
    Y = dataset.RawData['f']
    X = dataset.RawData['H']
    model = Probit(Y, X.astype(float))
    probit_model = model.fit()
    #a = probit_model.fittedvalues()
    #print(probit_model.summary())
    #print(np.mean(Probit.pdf(Y, X)))
    inverseM = -1*Probit.pdf(Y, X)/Probit.cdf(Y, X)
    #print(inverseM)
    return inverseM

def make_data():
    p = {}
    p['eta'] = 0.2
    p['a'] = 1
    p['gamma'] = 5
    p['delta'] = -0.2
    p['delta0'] = -0.1
    p['rho'] = 1
    d = FertilitySim(p, 10000)
    d.simulate()
    return d

def heckman(d):

    
    zeros = d.RawData[d.RawData['H']==0].index
    d.RawData.drop(zeros, inplace=True)
    Y = np.log(d.RawData['H'])
    X = np.array([d.RawData['X']]).reshape(len(Y), 1)
    print("Heckman-less values: ")
    regr = LinearRegression().fit(X, Y)
    print("regression coefficients for X: " + str(regr.coef_))
    print("regression intercept:" + str(regr.intercept_))
    print("regression score:" + str(regr.score(X, Y)))
    
    
    d.RawData['X'] = d.RawData['X']-(d.a * d.RawData['inverseM'])
    X = np.array([d.RawData['X']]).reshape(len(Y), 1)  
    print("With Heckman correction: ")
    regr = LinearRegression().fit(X, Y)
    print("regression coefficients for corrected X: " + str(regr.coef_))
    print("regression intercept:" + str(regr.intercept_))
    print("regression score:" + str(regr.score(X, Y)))

    

d = make_data()
#plt.hist(d.RawData['H'])
#plt.show()
#print(d.RawData)
print(np.mean(d.RawData['H']))
inverseM = probitfn(d)
d.RawData["inverseM"] = inverseM
heckman(d)
