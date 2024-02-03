import Functions

import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def random_neighbourhood_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_contant, constant_trading, news_relevance, stock_favorability, period_length):
    # initialize price list for market
    price_list = [initial_price]
    price_fluctuation = Functions.price_fluctuations(period_length, price_list)
    price_fluctuation_list = [price_fluctuation]
    trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
    trades_list = [trades]
    
    # initialize transaction quantities. Note that this implies at t=0 we initialize with imitators not trading and fundamentalists changing to the updated price values
    transaction_quantities = Functions.next_state_random_neighbourhood(trader_grid, np.zeros((L,L)), price_list, fundamental_value, news_relevance, L, trades)
    transactions = [transaction_quantities]
    for t in range(time):
        price_fluctuation = Functions.price_fluctuations(period_length, price_list)
        price_fluctuation_list.append(price_fluctuation)
        trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
        trades_list.append(trades)
        
        transactions.append(Functions.next_state_random_neighbourhood(trader_grid, transactions[-1], price_list, fundamental_value, news_relevance, L, trades))
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    return np.array(transactions), np.array(price_list), np.array(price_fluctuation_list), np.array(trades_list)


L = 100
fundamental_value = 100
initial_price = 100
time = 500
trader_grid = Functions.grid_stock_market(L, 0.3)
trading_constant = 20
news_relevance = [0.2, 0.7]
stock = 0.01
period = 10
sensitivity_constant = 0.7
sensitivity_variations = np.arange(0.2,1.2, 0.2)

resultS = random_neighbourhood_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_constant, trading_constant, news_relevance, stock, period)
plt.figure(dpi = 300)
plt.plot(np.arange(time+1), resultS[1], color = 'purple')
plt.xlabel('Time')
plt.ylabel('Price')
plt.suptitle('Price fluctuations of a single Stock')
plt.show()
plt.close()

plt.figure(dpi = 300)
plt.plot(np.arange(time+1), resultS[3], color = 'red')
plt.xlabel('Time')
plt.ylabel('Trading activity')
plt.suptitle('Trading activity')
plt.show()
plt.close()
    