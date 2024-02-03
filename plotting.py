import Functions

import numpy as np
import matplotlib.pyplot as plt

# Simulate level 3 for t time steps on given grid 
def Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_contant, constant_trading, news_relevance, stock_favorability, period_length):
    # initialize price list, price fluctuation storage, and trading activity for market
    price_list = [initial_price]
    price_fluctuation = Functions.price_fluctuations(period_length, price_list)
    price_fluctuation_list = [price_fluctuation]
    trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
    trades_list = [trades]
    
    # initialize transaction quantities. Note that this implies at t=0 we initialize with imitators not trading and fundamentalists changing to the updated price values
    transaction_quantities = Functions.next_state_Level_3(trader_grid, np.zeros((L,L)), price_list, fundamental_value, news_relevance, L, trades)
    transactions = [transaction_quantities[0]]
    News = [transaction_quantities[1]]
    # iterate CA model through time using next_state_level_3 function
    for t in range(time):
        # calulcate price fluctuation and trading activity at this time step
        price_fluctuation = Functions.price_fluctuations(period_length, price_list)
        price_fluctuation_list.append(price_fluctuation)
        trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
        trades_list.append(trades)
        
        # continue to next step in cellular automata and append next results
        next_result = Functions.next_state_Level_3(trader_grid, transactions[-1], price_list, fundamental_value, news_relevance, L, trades)
        transactions.append(next_result[0])
        News.append(next_result[1])
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    # return results as arrays: transaction matrix, prices, fluctuations in price, trading activity, and news relevance for fundamentalists and imitators
    return np.array(transactions), np.array(price_list), np.array(price_fluctuation_list), np.array(trades_list), np.array(News)


## MAP OF DIFFERENT REGIMES FOR NEWS RELEVANCE
# Regimes are minimal trading activity and increased trading activity
L = 20
fundamental_value = 100
initial_price = 100
time = 500
sensitivity_constant = 0.7
trader_grid = Functions.grid_stock_market(L, 0.5)
trading_constant = 20
# news_relevance = [0.2, 0.7]
stock = 0.01 
period = 10

# initialize storage for parameters, mean prices, and trading activity
Prices_matrix = []
Trading_activity_matrix = []

# initialize fundamentalist probability variations & iterate through different probabilities
Fundamentalist_news = np.arange(0,1.1, 0.1)
Imitator_news = np.arange(0,1.1, 0.1)
for fundamentalist_probability in Fundamentalist_news:
    # variate sensitivity constant
    Prices = []
    Trading = []
    print(fundamentalist_probability)
    for imitators_probability in Imitator_news:
        news_relevance = [fundamentalist_probability, imitators_probability]
        # initialize storage for each set of parameters and simulation results
        price_storage = []
        trading_activity_storage = []
        # simulate 30 times per parameter set for statistical significance
        for statistical_significance in range(20):
            simulation_results = Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_constant, trading_constant, news_relevance, stock, period)
            price_storage.append(np.mean(simulation_results[1]))
            trading_activity_storage.append(np.mean(simulation_results[3]))
        # append all results and parameters
        Prices.append(np.mean(price_storage))
        Trading.append(np.mean(trading_activity_storage))
    Prices_matrix.append(np.array(Prices))
    Trading_activity_matrix.append(np.array(Trading))


transitions_price = np.array(Prices_matrix)
transitions_trading_activity = np.array(Trading_activity_matrix)


# Generate phase transition map depending on sensitivity constant and fraction of fundamentalists
plt.imshow(transitions_trading_activity, extent=[min(Imitator_news), max(Imitator_news), min(Fundamentalist_news), max(Fundamentalist_news)], origin='lower', cmap='plasma_r')
plt.colorbar(label='Mean Trading Activity')
# Add labels and title
plt.xlabel('News relevance for Imitators')
plt.ylabel('News relevance for Fundamentalists')
plt.title('Phase Transition Map')
# Show the plot
plt.show()
