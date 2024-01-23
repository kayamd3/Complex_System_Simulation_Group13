import numpy as np
import matplotlib.pyplot as plt

# L is the length of the grid --> total size = L^2
# Fundamentalists are denoted by 0, imitators by 1
def grid_stock_market(L, fundamentalist_probability):
    # Generate an L by L array with random values between 0 and 1
    random_grid = np.random.rand(L, L)
    # Convert values to 0 or 1 based on the probability of a fundamentalist
    result_grid = (random_grid > fundamentalist_probability).astype(int)
    return result_grid

# Generate grid of traders
L = 25
probability_of_fundamentalist = 0.7
trader_grid = grid_stock_market(L, probability_of_fundamentalist)

# Plot trader type distribution
im = plt.imshow(trader_grid)
plt.show()

# Set up transition table
def transition_table(array):
    return np.mean(np.array(array))

# Set up function for state changes
def next_state(cur_state, price, fundamental_value):
    
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

# Transaction quantity
def calculation_transaction_quantity(transactions):
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

# Cellular auotmata through time 
time_steps = 2
initial_value = 100
initial_transaction_quantity = np.full((L, L), initial_value)
sensitivity_constant = 0.1
fundamental_value = 105

def market_simulation(time_steps, initial_price, initial_transaction_quantity, fundamental_value):
    price_list = [initial_price]
    current_state = [initial_transaction_quantity]
    assert (L,L) == np.shape(current_state[-1])
    
    for time in range(time_steps):
        current_state.append(next_state(current_state[-1], price_list[-1], fundamental_value))
        trans_quantity = calculation_transaction_quantity(current_state[-1])
        price_list.append(price_function(price_list[-1], sensitivity_constant, L, trans_quantity))
    return current_state, price_list

market_simulation(time_steps, 4, initial_transaction_quantity, fundamental_value)
        