'''
Microeconometrics hw 2
Max Marcussen
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels as sm
from statsmodels.discrete.discrete_model import Probit

class LaborSupplySim:
    """
        Class that constructs and simulates a static panel.
    """
    
    def __init__(self, param, num_ind=10000):
        
        """
            Initialize the class object.
            
            num_ind: Number of Individuals
            param: Parameter Set for Simulation
        """
        
        self.NumInd = num_ind  # Number of Individuals
        
        self.DataColumns = ['ID', 'X', 'Z', 'ϵ', 'u', 'ξ',
                            'W', 'R', 'β', 
                            'LFP', 'H']  
        
        self.γ = param['γ']
        self.β = param['β']
        self.a = param['a']
        self.ρ = param['ρ']
        self.η = param['η']
        self.δ = param['δ']
        self.δ0 = param['δ0']
        self.ν = param['ν']
        
        self.RawData = np.ndarray(shape=(self.NumInd, len(self.DataColumns)))
        self.PanelData = []
        self.LogFrame = []
        
        
    def simulate(self):
        
        """
            Generates the simulated data, and converts the NumPy array into a Pandas object.
        """
        
        # Worker ID
        self.RawData[:, 0] = np.arange(start=1, stop=self.NumInd+1, step=1, dtype=np.int8)
        
        # IID draws for observables from standard normal distribution
        self.RawData[:, 1] = np.random.randn(self.NumInd) # Draw for X
        self.RawData[:, 2] = np.random.randn(self.NumInd) # Draw for Z
        
        # IID draws for unobservables from normal distribution with variance 0.04
        self.RawData[:, 3] = 0.2 * np.random.randn(self.NumInd) # Draw for epsilon
        self.RawData[:, 4] = 0.2 * np.random.randn(self.NumInd) # Draw for u
        self.RawData[:, 5] = 0.2 * np.random.randn(self.NumInd) # Draw for xi
        
        # DGP for log W := eta * X + Z + u
        self.RawData[:, 6] = self.η * self.RawData[:, 1] + self.RawData[:, 2] + self.RawData[:, 4]
        
        # DGP for log R := delta_0 + log W + delta * Z + xi
        self.RawData[:, 7] = self.δ0 + self.RawData[:, 6] + self.δ * self.RawData[:, 2] + self.RawData[:, 5]
        
        # DGP for log beta := nu * X + a * xi + eps
        self.RawData[:, 8] = self.ν * self.RawData[:, 1] + self.RawData[:, 3] + self.a * self.RawData[:, 5]
                  
        # Determination of labor force participation (LFP)
        self.RawData[:, 9] = (np.log(self.ρ) + self.RawData[:, 6] - self.RawData[:, 7] >= 0)
        
        # Computing optimal number of hours worked
        self.RawData[:, 10] = np.power(np.divide(self.ρ * np.exp(self.RawData[:, 6]),
                                                 np.exp(self.RawData[:, 8])), 
                                       np.divide(1., self.γ)) * self.RawData[:, 9] 
        
        # Hiding wage details for non-participants in the labor market
        self.RawData[:, 6] = self.RawData[:, 6] * self.RawData[:, 9]     
        
        
        # Converstion to Pandas Dataframe
        panel_from_sim = pd.DataFrame(data=self.RawData, columns=self.DataColumns)

        # Establishing data types for each column of the Pandas DataFrame.
        panel_from_sim = panel_from_sim.astype({'ID': np.uint, 'X': np.float, 'Z': np.float,
                                                'ϵ': np.float, 'u': np.float, 'ξ': np.float, 
                                                'W': np.float, 'R': np.float, 'β': np.float,
                                                'LFP': np.uint, 'H': np.float})
        
        # panel_from_sim[['W', 'R', 'β']].applymap(np.exp)
        
        # Store RawData as a Pandas dataframe
        self.RawData = panel_from_sim.copy()
        
    def generate_panel(self):
        
        """
            Generates the panel with observables from the perspective of the econometrician.
        """
        
        self.PanelData = self.RawData.filter(['ID', 'X', 'Z', 'W', 'R', 'β', 'LFP', 'H'], axis=1)
        

def s(ind, dep):
    '''
    Simple regression fn.
    
    Inputs:
        ind: list of X terms to be regressed on.
        dep: dependent variable - string.
    Outputs:
        none - just prints regression statistics to the screen.
    '''
    p = {}
    p['γ'] = 0.8
    p['β'] = 1
    p['a'] = 1
    p['ρ'] = 1
    p['η'] = 0.2
    p['δ'] = -0.2
    p['δ0'] = -0.1
    p['ν'] = 0.5
    simdata = LaborSupplySim(p, 10000)
    simdata.simulate()
    simdata.generate_panel()
    zeros = simdata.PanelData[simdata.PanelData['H'] == 0].index
    simdata.PanelData.drop(zeros, inplace=True)
    simdata.PanelData['H'] = np.log(simdata.PanelData['H'])
    X = simdata.PanelData.filter(ind, axis=1)
    Y = simdata.PanelData[dep]
    regr = LinearRegression().fit(X, Y)
    print("regression coefficients for " + str(ind) + ": " + str(regr.coef_))
    print("regression intercept:" + str(regr.intercept_))
    print("regression score:" + str(regr.score(X, Y)))

def probit():
    '''
    A function for running the probit.
    '''
    p = {}
    p['γ'] = 0.8
    p['β'] = 1
    p['a'] = 0
    p['ρ'] = 1
    p['η'] = 0.2
    p['δ'] = -0.2
    p['δ0'] = -0.1
    p['ν'] = 0.5
    simdata_a0 = LaborSupplySim(p, 10000)
    simdata_a0.simulate()
    simdata_a0.generate_panel()
    
    Y = simdata_a0.PanelData['LFP']
    X = simdata_a0.PanelData['Z']
    model = Probit(Y, X.astype(float))
    probit_model = model.fit()
    print(probit_model.summary())
