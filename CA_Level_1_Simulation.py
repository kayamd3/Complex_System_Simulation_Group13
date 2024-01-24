import Functions

import numpy as np
import matplotlib.pyplot as plt


def Level_1_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_contant):
    # initialize price list for market
    price_list = [initial_price]
    # initialize transaction quantities. Note that this implies at t=0 we initialize with imitators not trading and fundamentalists changing to the updated price values
    transaction_quantities = Functions.next_state(trader_grid, np.zeros((L,L)), price_list[-1], fundamental_value, L)
    transactions = [transaction_quantities]
    for t in range(time):
        transactions.append(Functions.next_state(trader_grid, transactions[-1], price_list[-1], fundamental_value, L))
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    return np.array(transactions), np.array(price_list)


# Verification plots for Level 1 model
fundamentalists_probabilities = [0.2, 0.8]
L = 10
fundamental_value = 100
initial_price = 105
time = 100
constant = 0.5

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
    

trader_grid_presentation = Functions.grid_stock_market(L, 0.2)
# Plot trader type distribution
im = plt.imshow(trader_grid_presentation)
plt.show()
