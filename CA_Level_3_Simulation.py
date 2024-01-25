import Functions

import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

L = 10**2
fundamental_value = 100
initial_price = 100
time = 1000
sensitivity_constant = 0.7
trader_grid = Functions.grid_stock_market(L, 0.3)
trading_constant = 20
news_relevance = [0.2, 0.7]
stock = 0.01
period = 10


resultS = Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_constant, trading_constant, news_relevance, stock, period)
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

## NOTES: 
    # Maybe vary connection probability in random graph to observe how that would affect the trading behaviour 
    # and price fluctuation --> see if you can also observe a change in pricing/trading behaviour
    # Algorithmic complexity in order to quantify the complexity observed?
    # Look into early warning signs of phase transitions --> paper on critical points
    # Coul you make a bifurcation diagram for this transition?
    # Control parameter vs order parameter plot ?
    # Potential expansion of model could be to implement the spread of rumors in the model --> how does this affect simulation
    
## PHASE TRANSITIONS
# First generate means for different sensitivity constants
# Initialize storage of order parameters
average_price = []
price_variance = []
average_trading_activity = []
trading_activity_variance = []

# Generate order parameters for varying control parameter
sensitivity_variations = np.arange(0.5,1.1, 0.1)
for sensitivity in sensitivity_variations:
    price_storage = []
    trading_activity_storage = []
    for statistical_significance in range(30):
        simulation_result = Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity, trading_constant, news_relevance, stock, period)
        price_storage.append(np.mean(simulation_result[1]))
        trading_activity_storage.append(np.mean(simulation_result[3]))
    average_price.append(np.mean(price_storage))
    price_variance.append(np.std(price_storage))
    average_trading_activity.append(np.mean(trading_activity_storage))
    trading_activity_variance.append(np.std(trading_activity_storage))

ci_price = 1.96 * np.array(price_variance)/30
ci_trading_activity = 1.96 * np.array(trading_activity_variance)/30

plt.figure(dpi = 300, figsize = (4, 8))

plt.subplot(211)
plt.plot(sensitivity_variations, average_price, color = 'purple')
plt.fill_between(sensitivity_variations, (np.array(average_price)-ci_price), (np.array(average_price)+ci_price), color='purple', alpha=.25)
plt.ylabel('Mean price')
plt.subplot(212)
plt.plot(sensitivity_variations, average_trading_activity, color = 'red')
plt.fill_between(sensitivity_variations, (np.array(average_trading_activity)-ci_trading_activity), (np.array(average_trading_activity)+ci_trading_activity), color='red', alpha=.25)
plt.ylabel('Mean trading activity')
plt.xlabel('Sensitivity constant')
plt.show()
plt.close()

# Price transitions: we observe that for sensitivity > 1.1 the mean price fluctuates
# a lot more --> potentially interesting to create a confidence interval to have an area in which the mean 
# price is expected to lie

# Trading activity: for all runs so far it has been observed that the trading activity is minimal if 
# the sensitivity constant is below 0.7. Note that this aligns nicely with the results observed yesterday as well.

#######################################################
#######################################################
#######################################################
#### TRIAL TO CREATE 2 SUPLOTS WITH THE SAME SLIDER
fig = make_subplots(rows=2, cols=1,shared_xaxes=True) # ,vertical_spacing  = 0.25

# Add traces, one for each slider step
for sensitivity in sensitivity_variations:
    results = Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity, trading_constant, news_relevance, stock, period)
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="purple", width=2),
            name="Sensitivity" + str(sensitivity),
            x = np.arange(0, len(results[1])+1, 1.0),
            y = results[1]
            ),row=1, col=1)
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="red", width=2),
            name="Sensitivity " + str(sensitivity),
            x = np.arange(0, len(results[1])+1, 1.0),
            y = results[3]
            ),row=2, col=1)


# Create and add slider
steps = []

for i in range(0, len(fig.data), 2):
    step = dict(
        method="restyle",
        args=["visible", [False] * len(fig.data)],
    )
    step["args"][1][i:i+2] = [True, True]
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time:  "},
    pad={"t": 50},
    steps=steps
)]

fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Trading Activity", row=2, col=1)
fig.update_layout(sliders=sliders, title="Prices & Trading Activity for varying sensitivity constant", template ="plotly_white")

plotly.offline.plot(fig, filename='Phases_SensitivityConstant.html')
fig.show() 