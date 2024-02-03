import numpy as np
import random

# Generate grid of traders
def grid_stock_market(L, fundamentalist_probability):
    # Generate an L by L array with random values between 0 and 1
    random_grid = np.random.rand(L, L)
    # Convert values to 0 or 1 based on the probability of a fundamentalist
    result_grid = (random_grid > fundamentalist_probability).astype(int)
    return result_grid

# Required for all levels
# Set up transition table
def transition_table(array):
    return np.mean(np.array(array))

# Transaction quantity
def calculation_transaction_quantity(transactions, L):
    total_transactions = 0
    for row in range(L):
        for column in range(L):
            total_transactions = total_transactions + transactions[row, column]
    return total_transactions

# Price function 
def price_function(previous_price, sensitivity_contant, L, transaction_quantity):
    price = previous_price + sensitivity_contant*transaction_quantity/(L**2)
    if price < 0 :
        price = 0
    return price

# Set up function for state changes (Level 1)
def next_state(trader_grid, cur_state, price, fundamental_value, L):
    
    transaction_quantity = np.zeros(np.shape(cur_state))
    assert (L, L) == np.shape(cur_state)
    
    for row_index in range(L):
        for column_index in range(L):
            trader_type = trader_grid[row_index, column_index]
            if trader_type == 0:
                transaction_quantity[row_index,column_index] = fundamental_value - price
            else: 
                transaction_quantity[row_index,column_index] = transition_table([cur_state[(row_index-1)%L, column_index%L], cur_state[(row_index+1)%L, column_index%L], cur_state[(row_index)%L, (column_index-1)%L], cur_state[(row_index)%L, (column_index+1)%L], cur_state[(row_index-1)%L, (column_index-1)%L], cur_state[(row_index-1)%L, (column_index+1)%L], cur_state[(row_index+1)%L, (column_index-1)%L],cur_state[(row_index+1)%L, (column_index+1)%L]])
    
    return transaction_quantity

# Expansion for function of level 2
def news_influence(parameters):
    c_fundamentalist, c_imitator = parameters
    factor_news_fundamentalist = 1 + c_fundamentalist*np.random.normal(loc = 0.0, scale = 1.0)
     
    factor_news_imitator = 1 + c_imitator*np.random.normal(loc = 0.0, scale = 1.0)
    factor_news = [factor_news_fundamentalist, factor_news_imitator]
    return np.array(factor_news)

def next_state_Level_2(trader_grid, cur_state, price_list, fundamental_value, news_relevance, L):
    
    transaction_quantity = np.zeros(np.shape(cur_state))
    assert (L, L) == np.shape(cur_state)
    news_both = news_influence(news_relevance)
    for row_index in range(L):
        for column_index in range(L):
            trader_type = trader_grid[row_index, column_index]
            
            if trader_type == 0:
                price = price_list[-1]
                news = news_both[0]
                transaction_quantity[row_index,column_index] = (fundamental_value*news - price)
            else: 
                news = news_both[1]
                transaction_quantity[row_index,column_index] = news*transition_table([cur_state[(row_index-1)%L, column_index%L], cur_state[(row_index+1)%L, column_index%L], cur_state[(row_index)%L, (column_index-1)%L], cur_state[(row_index)%L, (column_index+1)%L], cur_state[(row_index-1)%L, (column_index-1)%L], cur_state[(row_index-1)%L, (column_index+1)%L], cur_state[(row_index+1)%L, (column_index-1)%L],cur_state[(row_index+1)%L, (column_index+1)%L]])
    
    return transaction_quantity

# Expansion for level 3
def price_fluctuations(k, prices):
    k = min(k, len(prices))
    P_bar = sum(prices[-k:]) / k  # Calculate the average price
    Lt = sum(abs(P_i - P_bar) for P_i in prices[-k:]) / (k*P_bar)
    return Lt

    
def trading_activity_function(Cl, Lt, Lm):
    """
    Calculate the current trading activity M^t.

    :param Lt: Current price volatility level
    :param Cl: Parameter
    :param Lm: Threshold
    :return: Current trading activity level
    """
    # The lower bound of Mt is 0.05
    # return 1.1
    if Lt <= Lm:
        return max(Cl * Lt, 0.05)
    else:
        return max(Cl * (-Lt + 2 * Lm), 0.05)
    

def next_state_Level_3(trader_grid, cur_state, price_list, fundamental_value, news_relevance, L, trades):
    
    transaction_quantity = np.zeros(np.shape(cur_state))
    assert (L, L) == np.shape(cur_state)
    
    news_both = news_influence(news_relevance)
    for row_index in range(L):
        for column_index in range(L):
            trader_type = trader_grid[row_index, column_index]
            
            if trader_type == 0:
                price = price_list[-1]
                news = news_both[0]
                transaction_quantity[row_index,column_index] = (fundamental_value*news - price) * trades
            else:
                news = news_both[1]
                transaction_quantity[row_index,column_index] = trades*news*transition_table([cur_state[(row_index-1)%L, column_index%L], cur_state[(row_index+1)%L, column_index%L], cur_state[(row_index)%L, (column_index-1)%L], cur_state[(row_index)%L, (column_index+1)%L], cur_state[(row_index-1)%L, (column_index-1)%L], cur_state[(row_index-1)%L, (column_index+1)%L], cur_state[(row_index+1)%L, (column_index-1)%L],cur_state[(row_index+1)%L, (column_index+1)%L]])
    
    return transaction_quantity, news_both


def next_state_random_neighbourhood(trader_grid, cur_state, price_list, fundamental_value, news_relevance, L, trades, neighbourhood_row, neighbourhood_column):
    
    transaction_quantity = np.zeros(np.shape(cur_state))
    assert (L, L) == np.shape(cur_state)
    
    news_both = news_influence(news_relevance)
    for row_index in range(L):
        for column_index in range(L):
            trader_type = trader_grid[row_index, column_index]
            
            if trader_type == 0:
                price = price_list[-1]
                news = news_both[0]
                transaction_quantity[row_index,column_index] = (fundamental_value*news - price) * trades
            else:
                news = news_both[1]
                transaction_quantity[row_index,column_index] = trades*news*transition_table([cur_state[neighbourhood_row[row_index], neighbourhood_column[column_index]]])
    
    return transaction_quantity





