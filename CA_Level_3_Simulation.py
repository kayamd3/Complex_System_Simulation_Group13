import Functions

import numpy as np
import matplotlib.pyplot as plt

def Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_contant, constant_trading, news_relevance, stock_favorability, period_length):
    # initialize price list for market
    price_list = [initial_price]
    price_fluctuation = Functions.price_fluctuations(period_length, price_list)
    price_fluctuation_list = [price_fluctuation]
    trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
    trades_list = [trades]
    
    # initialize transaction quantities. Note that this implies at t=0 we initialize with imitators not trading and fundamentalists changing to the updated price values
    transaction_quantities = Functions.next_state_Level_3(trader_grid, np.zeros((L,L)), price_list, fundamental_value, news_relevance, L, trades)
    transactions = [transaction_quantities]
    for t in range(time):
        price_fluctuation = Functions.price_fluctuations(period_length, price_list)
        price_fluctuation_list.append(price_fluctuation)
        trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
        trades_list.append(trades)
        
        transactions.append(Functions.next_state_Level_3(trader_grid, transactions[-1], price_list, fundamental_value, news_relevance, L, trades))
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    return np.array(transactions), np.array(price_list), np.array(price_fluctuation_list), np.array(trades_list)

L = 100
fundamental_value = 100
initial_price = 100
time = 1000
constant = 0.7
trader_grid = Functions.grid_stock_market(L, 0.3)
constant_trading = 20
news_relevance = [0.2, 0.7]
stock = 0.01
period = 10


resultS = Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, constant, constant_trading, news_relevance, stock, period)
plt.figure(dpi = 300)
plt.plot(np.arange(time+1), resultS[1])
plt.show()
plt.close()

plt.figure(2)
plt.plot(np.arange(time+1), resultS[3])
plt.show()
plt.close()

## NOTES: 
    # Maybe vary connection probability in random graph to observe how that would affect the trading behaviour 
    # and price fluctuation --> see if you can also observe a change in pricing/trading behaviour
    # Algorithmic complexity in order to quantify the complexity observed?
    # Look into early warning signs of phase transitions --> paper on critical points
    # Coul you make a bifurcation diagram for this transition?
    # Control parameter vs order parameter plot ?
    # Potential expansion of model could be to implement the spread of rumors in the model --> how does this affect simulation