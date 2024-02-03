import numpy as np

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

# Transaction quantity per time step 
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
    # initialize new transaction quantity matrix
    transaction_quantity = np.zeros(np.shape(cur_state))
    # test if size remained the same in each step
    assert (L, L) == np.shape(cur_state)
    # iterate through each trader on the grid
    for row_index in range(L):
        for column_index in range(L):
            # verify trader type of current position and update transaction quantity accordingly
            trader_type = trader_grid[row_index, column_index]
            if trader_type == 0:
                transaction_quantity[row_index,column_index] = fundamental_value - price
            else: 
                transaction_quantity[row_index,column_index] = transition_table([cur_state[(row_index-1)%L, column_index%L], cur_state[(row_index+1)%L, column_index%L], cur_state[(row_index)%L, (column_index-1)%L], cur_state[(row_index)%L, (column_index+1)%L], cur_state[(row_index-1)%L, (column_index-1)%L], cur_state[(row_index-1)%L, (column_index+1)%L], cur_state[(row_index+1)%L, (column_index-1)%L],cur_state[(row_index+1)%L, (column_index+1)%L]])
    # return matrix of transaction quantities
    return transaction_quantity

# Expansion for function of level 2
# Define function modelling the news influence
def news_influence(parameters):
    # different news influence factors
    c_fundamentalist, c_imitator = parameters
    # different relevance factor news plays in current time step
    factor_news_fundamentalist = 1 + c_fundamentalist*np.random.normal(loc = 0.0, scale = 1.0)
    factor_news_imitator = 1 + c_imitator*np.random.normal(loc = 0.0, scale = 1.0)
    factor_news = [factor_news_fundamentalist, factor_news_imitator]
    return np.array(factor_news)

# calculate next state of CA for Level 2 model (including the news)
def next_state_Level_2(trader_grid, cur_state, price_list, fundamental_value, news_relevance, L):
    # initialize new transaction quantity list 
    transaction_quantity = np.zeros(np.shape(cur_state))
    # test size
    assert (L, L) == np.shape(cur_state)
    # define news fators in this step 
    news_both = news_influence(news_relevance)
    # iterate through trader grid and test trader type
    for row_index in range(L):
        for column_index in range(L):
            trader_type = trader_grid[row_index, column_index]
            # update transaction quantity per trader depending on its type
            if trader_type == 0:
                price = price_list[-1]
                news = news_both[0]
                transaction_quantity[row_index,column_index] = (fundamental_value*news - price)
            else: 
                news = news_both[1]
                transaction_quantity[row_index,column_index] = news*transition_table([cur_state[(row_index-1)%L, column_index%L], cur_state[(row_index+1)%L, column_index%L], cur_state[(row_index)%L, (column_index-1)%L], cur_state[(row_index)%L, (column_index+1)%L], cur_state[(row_index-1)%L, (column_index-1)%L], cur_state[(row_index-1)%L, (column_index+1)%L], cur_state[(row_index+1)%L, (column_index-1)%L],cur_state[(row_index+1)%L, (column_index+1)%L]])
    # return matrix of different transaction quantities
    return transaction_quantity

# Expansion for level 3
# include price fluctuations
def price_fluctuations(k, prices):
    k = min(k, len(prices))
    P_bar = sum(prices[-k:]) / k  # Calculate the average price
    Lt = sum(abs(P_i - P_bar) for P_i in prices[-k:]) / (k*P_bar)
    return Lt
   
# include price fluctuations 
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
    
# update next state for level 3 model, including news, price fluctuations and varying trading activity
def next_state_Level_3(trader_grid, cur_state, price_list, fundamental_value, news_relevance, L, trades):
    # initialize next state transaction quantity matrix and assert whether it has the same size as trader grid
    transaction_quantity = np.zeros(np.shape(cur_state))
    assert (L, L) == np.shape(cur_state)
    # calculate news for this time step
    news_both = news_influence(news_relevance)
    
    # update grid depending on trader type
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
    # return matrix of all transaction quantities as well as news factors
    return transaction_quantity, news_both

# twist of original model: now randomize original moore neighbourhood to be a random rewiring to one other trader on the grid
# rewiring is only done once
def next_state_random_neighbourhood(trader_grid, cur_state, price_list, fundamental_value, news_relevance, L, trades, neighbourhood_row, neighbourhood_column):
    # initialize next state transaction quantity
    transaction_quantity = np.zeros(np.shape(cur_state))
    assert (L, L) == np.shape(cur_state)
    # calculate news relevance for this time step and update the grid accordingly
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
                # neighbourhood_row and neighbourhood_column are passed in as arguments in this simulation
                # they are random integers which represent the indices of the traders the imitator is looking at
                transaction_quantity[row_index,column_index] = trades*news*transition_table([cur_state[neighbourhood_row[row_index], neighbourhood_column[column_index]]])
    # return matrix of new transaction quantities
    return transaction_quantity

# Calculate the returns for the prices
def calculate_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        returns.append((prices[i] - prices[i - 1]) / prices[i - 1])
    return returns

# Divides the returns in different bins and calculates the variance for each bin
def variance_of_bins(returns, num_bins):
    smaller_lists = []
    bins_variances = []
    bin_size = int(len(returns) / num_bins)
    for i in range(0, len(returns), bin_size):
        smaller_lists.append(returns[i:i + bin_size])
        bins_variances.append(np.var(returns[i:i + bin_size]))
    return bins_variances




