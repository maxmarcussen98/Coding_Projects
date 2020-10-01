import numpy as np 
import pandas as pd 
from pandas_datareader import data as wb
from iexfinance.base import _IEXBase
from iexfinance import Stock, StockReader
from urllib.parse import quote
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import progressbar
import time
import util

api = tradeapi.REST()

def buy(symbol, quantity):
    '''
    Buyer function
    '''
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='day')

def sell(symbol, quantity):
    '''
    Seller function
    '''
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='day')