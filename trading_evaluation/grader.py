import pandas as pd
from collections import Counter

STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'IBM', 'AMZN']

def read_stock_price (stock, start_date, end_date, file_path = './data/'):
    '''
    start_date and end_date needs to be in format of "2018-01-30"
    '''
    file_path = file_path + stock + '.csv'
    df = pd.read_csv (file_path)
    res = df[(df.Date >= start_date) & (df.Date <= end_date)]
    return res

def do_nothing_strategy (stock_info):
    res = dict()
    for stock in stock_info.keys():
        res[stock] = 0
    return res

def eval_trading_strategy (stock_list, start_date, end_date, init_amount, trading_strategy = do_nothing_strategy):
    # init a portfolio, all start with 0 stocks
    portfolio = dict()
    for stock in stock_list:
        portfolio[stock] = 0

    # variable to keep track of remaining money
    cur_amount = init_amount

    all_stock_info = dict()
    nb_trading = 0
    for stock in stock_list:
        stock_info = read_stock_price (stock, start_date, end_date)
        all_stock_info [stock] = stock_info
        nb_trading = stock_info.shape[0]

    for i in range (nb_trading - 1):
        one_day_info = dict()
        for stock in stock_list:
            one_day_stock_info = all_stock_info[stock].iloc[[i]]
            one_day_info[stock] = one_day_stock_info
        decision = trading_strategy (one_day_info)

        # update portfolio
        for stock in stock_list:
            portfolio[stock] += decision[stock]
            cur_amount -= decision[stock] * one_day_info[stock].iloc[0]['Adj Close']
            assert (portfolio[stock] >= 0)

    return cur_amount, portfolio

if __name__ == '__main__':
    last_amount, last_portfolio = eval_trading_strategy(STOCKS, "2018-12-31", "2019-05-31", 1e6)
    print (last_amount)
    print (last_portfolio)