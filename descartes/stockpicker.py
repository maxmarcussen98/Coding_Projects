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

#this is the version WITHOUT finding graham fundamental stocks from sectors

def get_sp():
    sp_list = []
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    
    sliced_table = data.iloc[:,1]
    for row, index in sliced_table.iteritems():
        sp_list.append(index)
    return sp_list


def markowitz(assets, pfolio_size):
    '''
    Our Markowitz efficient frontier function.
    Randomly weights every stock we have a given number of times.
        -this number just needs to be enough that we can find a low-risk,
        high-return portfolio that'll be similar enough in weights
        to yesterday's. For now, 100000.
    '''
    
    start_date = '2018-5-1'
    num_tests = 20000
    pf_data = pd.DataFrame()

    print("Retrieving data...")
    for a in assets:
        pf_data[a] = wb.DataReader(a, data_source = 'yahoo', start = start_date)['Adj Close']
    print("Data retrieved")

    log_returns = np.log(pf_data / pf_data.shift(1))

    num_assets = len(assets)

    # we're going to do 1000 combinations
    pfolio_returns = []
    pfolio_volatilities = []
    pfolio_weights = []
    curr_best = -8000
    best_returns = -1000
    best_vol = 1
    best_weights = []

    #below is a progress bar - unfortunately we can't use progress
    #bars for our deployment so we'll just comment it out
    #bar = progressbar.ProgressBar(max_value=num_tests)

    for x in range (num_tests):
        #bar.update(x)
        percent = num_tests // 10
        if x % percent == 0:
            print(str(x // percent) + "0% tested")
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        pfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
        pfolio_volatilities.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))
        pfolio_weights.append(weights)
        returns = (np.sum(weights*log_returns.mean())*250)
        volatility = (np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))
        ratio = returns/volatility
        if ratio > curr_best:
            is_weighted_good = True
            for w in weights:
                '''
                MUST MODIFY MAXIMUM WEIGHT EACH EQUITY CAN
                TAKE IN LINE BELOW
                '''
                if w * pfolio_size > 1.7:
                    is_weighted_good = False
            if is_weighted_good:
                curr_best = ratio
                best_weights = weights
                best_returns = returns
                best_vol = volatility
    #turn this into a numpy array
    pfolio_returns = np.array(pfolio_returns)
    pfolio_volatilities = np.array(pfolio_volatilities)
    weights_dict = {}
    for i in range(0, len(best_weights)):
        weights_dict[assets[i]] = best_weights[i]

    portfolios = pd.DataFrame({'Return': pfolio_returns, 'Volatility': pfolio_volatilities, 
        'Weights': pfolio_weights})

    print("Return of this portfolio since " + start_date + ": " + str(best_returns))
    print("Volatility of this portfolio since " + start_date + ": " + str(best_vol))

    portfolios.plot(x='Volatility', y='Return', kind='scatter', figsize=(10, 6))
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    # plt.show()
    print(weights_dict)
    return weights_dict

def percents_to_equity(weights_dict, curr_equity):
    equity_dict = {}
    for stock in weights_dict:
        equity_dict[stock] = weights_dict[stock] * curr_equity
    return equity_dict

def make_list_good_stocks(my_stocks, sp):
    # this is the version WITHOUT fundamentals

    # make a list of all the stocks in s&p plus our own list

    print("Making list of investments...")
    stock_list = my_stocks.copy()
    for stock in sp:
        if stock not in stock_list:
            stock_list.append(stock)
    return stock_list

def find_moving_avg(data):
    '''
    Finds the moving average for past 3 days in comparison with past 45 days.
    '''
    ShortAvg = data.tail(3).mean()
    LongAvg = data.tail(45).mean()
    percent_difference = (ShortAvg - LongAvg) / LongAvg
    return percent_difference

def make_new_weights(option_list, pfolio_size, portfolio, replace_rate, pfolio_equity):
    '''
    Finds the stocks that are overweight and replaces with underweight.
    Then calls markowitz function to find best weights for each stock in our pfolio.
    Underweight and overweight determined by 3 day moving avg. vs 45 day.
    '''
    print("Rebalancing for underweighted stocks...")
    avg_dict = {}
    print(pfolio_equity)
    print(pfolio_size)

    #create a data frame of the moving averages 
    for stock in option_list:
        try:
            past_year_closes = StockReader.get_chart(Stock(stock, 
                output_format = 'pandas'), range = '1y')['close']
            if past_year_closes.tail(3).mean() < 1.5 * pfolio_equity / pfolio_size:
                avg_dict[stock] = find_moving_avg(past_year_closes)
        except:
            pass
    avg_df = pd.DataFrame.from_dict(avg_dict, orient='index', columns = 
        ['3 day moving average vs. 45 day']).sort_values('3 day moving average vs. 45 day',
        ascending=False)

    # new buy list

    new_buy_list = portfolio.copy()

    list_to_sell = []

    print("Removing overweight stocks...")
    num_to_remove = int(pfolio_size * replace_rate)
    num_removed = 0
    if len(new_buy_list) > num_to_remove:
        for index, row in avg_df.iterrows():
            if index in new_buy_list:
                print(index)
                new_buy_list.pop(new_buy_list.index(index))
                list_to_sell.append(index)
                num_removed += 1
                if num_removed == num_to_remove:
                    break
    sell_leftovers(list_to_sell)
    
    print("Adding underweight stocks...")
    num_to_replace = pfolio_size - len(new_buy_list)
    num_added = 0
    avg_df = avg_df.sort_values('3 day moving average vs. 45 day', ascending=True)
    if len(new_buy_list) < pfolio_size:
        for index, row in avg_df.iterrows():
            if index not in new_buy_list:
                new_buy_list.append(index)
                print(index + " added")
                num_added += 1
            if num_added == num_to_replace:
                break
    
    print("stock buy list:")
    print(new_buy_list)

    print("Running efficient frontier analysis...")
    best_weights = markowitz(new_buy_list, pfolio_size)

    return best_weights

def sell_leftovers(list_to_sell):
    '''
    Sells all of the stocks that are in our overweight list.
    '''
    for symbol in list_to_sell:
        position = api.get_position(symbol)
        quantity = position.qty
        print('submit(sell): ' + str(quantity) + ' shares of ' + symbol)
        try:
            util.sell(symbol, quantity)
        except:
            print("No trade due to pattern day trading")

    return None

def buy_portfolio(equity_values):
    '''
    Buys our portfolio.
    Sells everything that we want to reduce the weight of first, then
    buys everything we want to increase weight of.

    If an order doesn't fill all the way, it expires at end of day.

    We calculate number of shares to buy by dividing equity value we
    got by the current price.
    '''
    time.sleep(10)
    buy_dict = {}
    sell_dict = {}

    portfolio = []
    for position in api.list_positions():
        portfolio.append(position.symbol)

    bought_so_far = 0
    for symbol in equity_values:
        equity=equity_values[symbol]
        quantity = int(equity // Stock(symbol).get_price())
        if symbol in portfolio:
            quantity -= int(api.get_position(symbol).qty)
        if quantity > 0:
            buy_dict[symbol] = quantity
        elif quantity < 0:
            sell_dict[symbol] = quantity

    for symbol in sell_dict:
        quantity = sell_dict[symbol]
        time.sleep(10)
        quantity = abs(quantity)
        print('submit(sell): ' + str(quantity) + ' shares of ' + symbol)
        print(str(quantity * Stock(symbol).get_price()) + ' sold')
        try:
            util.sell(symbol, quantity)
        except:
            print("Not sold due to an error.")

    for symbol in buy_dict:
        quantity = buy_dict[symbol]
        time.sleep(10)
        print('submit(buy): ' + str(quantity) + ' shares of ' + symbol)
        new_bought = quantity * Stock(symbol).get_price()
        bought_so_far += new_bought
        print(str(new_bought) + " of " + symbol + " bought ")
        print("new portfolio value bought so far: $" + str(bought_so_far))
        try:
            util.buy(symbol, quantity)
        except:
            print("Not bought due to an error.")
        
    return None

def main():
    '''
    Our Main function. Once a day, goes through all of our logic.
    '''
    
    #first, define all our variables.
   
    pfolio_size = 10
    replace_rate = 0.2

    my_stocks = ['NFLX', 'SQ', 'FB', 'VWO', 'CGC', 'ADBE', 'BABA', 'NVDA', 'AMD', 
        'NKE', 'DIS', 'SBUX', 'BAC', 'SNAP', 'TSLA', 'TWTR', 'BYND', 'SMFG']
    
    sp = get_sp()

    '''
    now we have our main logic.
    check if market is open every minute. if it is:
        define more variables we'll use in our logic today.
        make a list of the best stocks to buy (those with good Graham
        fundamentals plus our hand picked ones).
        determine which we want to sell and which we want to buy out of these. sell
        those that are overpriced for past 3 days compared to past 45, buy those that
        are cheaper for last 3 days compared with past 45.
        Finds best weights for each stock we've picked.
        Buys each of those weights.
    '''
    done = None
    days_since_trade = 1
    print('start running')
    while True:
        # clock API returns the server time including the
        # boolean flag for market open
        # all times are expressed in universal time
        clock = api.get_clock()
        now = clock.timestamp
        if clock.is_open and done != now.strftime('%Y-%m-%d'):
            portfolio = []
            for position in api.list_positions():
                portfolio.append(position.symbol)

            pfolio = api.get_account()
            pfolio_equity = float(pfolio.portfolio_value)
            
            # find our list of stocks to consider - includes our Graham stocks
            # and our personal picks
            stocks_to_invest = make_list_good_stocks(
                my_stocks,
                sp)

            # determine which stocks are underweighted and our best picks - 
            # sell stocks that are overweighted
            weights_to_buy = make_new_weights(
                stocks_to_invest, 
                pfolio_size, 
                portfolio, 
                replace_rate,
                pfolio_equity)

            # give back equity values of stocks to buy
            equity_values = percents_to_equity(
                weights_to_buy, 
                pfolio_equity)

            # buying and selling logic for getting to equity
            # values we want
            buy_portfolio(
                equity_values)

            # sets done to our date and prevents this if logic from being called again today
            done = now.strftime('%Y-%m-%d')
            print(f'done for {done}')

        time.sleep(60)

if __name__ == '__main__':
    main()
