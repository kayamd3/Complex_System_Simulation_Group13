import Functions

import numpy as np
import matplotlib.pyplot as plt

# Simulate level one for t time steps on given grid 
def Level_1_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_contant):
    # initialize price list for market
    price_list = [initial_price]
    # initialize transaction quantities. Note that this implies at t=0 we initialize with imitators not trading and fundamentalists changing to the updated price values
    transaction_quantities = Functions.next_state(trader_grid, np.zeros((L,L)), price_list[-1], fundamental_value, L)
    transactions = [transaction_quantities]
    # update transaction quantities for time steps
    for t in range(time):
        transactions.append(Functions.next_state(trader_grid, transactions[-1], price_list[-1], fundamental_value, L))
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    # return array of transaction quantities and prices over time
    return np.array(transactions), np.array(price_list)


# Set initial conditions for the simulation
fundamentalists_probabilities = [0.2, 0.8]
L = 50
fundamental_value = 100
initial_price = 105
time = 100
constant = 0.5

# plot prices for different distributions of fundamentalist and imitator
plt.figure(dpi = 300)
for p in fundamentalists_probabilities:
    trader_grid = Functions.grid_stock_market(L, p)
    prices = Level_1_simulation(trader_grid, initial_price, fundamental_value, time, L, constant)
    plt.plot(np.arange(time + 1), prices[1], label = p)
plt.suptitle('Stock prices for varying distributions of fundamentalists and imitators')
plt.xlabel('Time')
plt.ylabel('Stock price')
plt.legend()
plt.show()
plt.close()
    

# Generate trader grid for presentation
trader_grid_presentation = Functions.grid_stock_market(L, 0.5)
# Plot trader type distribution
plt.figure(dpi = 300)
im = plt.imshow(trader_grid_presentation, origin="lower")
ax = plt.gca();
# Minor ticks
ax.set_xticks(np.arange(-.5, 50, 1), minor=True)
ax.set_yticks(np.arange(-.5, 50, 1), minor=True)
# Gridlines based on minor ticks
ax.grid(which='minor', color='black', linestyle='-', linewidth=0.2)
#plt.title('Representation of the trader grid')
plt.show()
