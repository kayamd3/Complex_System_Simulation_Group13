import Functions

import numpy as np
import matplotlib.pyplot as plt


def Level_2_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_contant, news_relevance):
    # initialize price list for market
    price_list = [initial_price]
    
    # initialize transaction quantities. Note that this implies at t=0 we initialize with imitators not trading and fundamentalists changing to the updated price values
    transaction_quantities = Functions.next_state_Level_2(trader_grid, np.zeros((L,L)), price_list, fundamental_value, news_relevance, L)
    transactions = [transaction_quantities]
    for t in range(time):
    
        transactions.append(Functions.next_state_Level_2(trader_grid, transactions[-1], price_list, fundamental_value, news_relevance, L))
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    return np.array(transactions), np.array(price_list) 

L = 10
fundamental_value = 100
initial_price = 100
time = 100
constant = 0.05
trader_grid = Functions.grid_stock_market(L, 0.3)
constant_trading = 20
news_relevance = [0.2, 0.7]
stock = 0.01
period = 400


resultS = Level_2_simulation(trader_grid, initial_price, fundamental_value, time, L, constant, news_relevance)
plt.figure(dpi = 300)
plt.plot(np.arange(time+1), resultS[1])
plt.show()
plt.close()
