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
    transactions = [transaction_quantities[0]]
    News = [transaction_quantities[1]]
    for t in range(time):
        price_fluctuation = Functions.price_fluctuations(period_length, price_list)
        price_fluctuation_list.append(price_fluctuation)
        trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
        trades_list.append(trades)
        
        next_result = Functions.next_state_Level_3(trader_grid, transactions[-1], price_list, fundamental_value, news_relevance, L, trades)
        transactions.append(next_result[0])
        News.append(next_result[1])
        trans_quantity = Functions.calculation_transaction_quantity(transactions[-1], L)
        price_list.append(Functions.price_function(price_list[-1],sensitivity_contant,L, trans_quantity))
    return np.array(transactions), np.array(price_list), np.array(price_fluctuation_list), np.array(trades_list), np.array(News)

L = 50
fundamental_value = 100
initial_price = 100
time = 500
sensitivity_constant = 0.7
trader_grid = Functions.grid_stock_market(L, 0.5)
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

Fundamentalist_news = np.arange(0,1.1, 0.1)    

fig = make_subplots(rows=2, cols=1,shared_xaxes=True)
# Add traces, one for each slider step
for news_fundamentalists in Fundamentalist_news:
    news_relevance = [news_fundamentalists, 0.5]
    results = Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_constant, trading_constant, news_relevance, stock, period)
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="purple", width=2),
            name="News" + str(news_fundamentalists),
            x = np.arange(0, len(results[1])+1, 1.0),
            y = results[1]
            ),row=1, col=1)
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="red", width=2),
            name="News " + str(news_fundamentalists),
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
fig.update_layout(sliders=sliders, title="Prices & Trading Activity for varying News relevance", template ="plotly_white")

plotly.offline.plot(fig, filename='Phases_NewsRelevance.html')
fig.show() 
    
## PHASE TRANSITIONS
# First generate means for different sensitivity constants
# Initialize storage of order parameters
L = 10
fundamental_value = 100
initial_price = 100
time = 100
sensitivity_constant = 0.7
trader_grid = Functions.grid_stock_market(L, 0.5)
trading_constant = 20
news_relevance = [0.2, 0.7]
stock = 0.01
period = 10

average_price = []
price_variance = []
average_trading_activity = []
trading_activity_variance = []


sensitivity_variations = np.arange(0.2, 1.4, 0.2)
# Generate order parameters for varying control parameter
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
plt.suptitle('Emergence of Price fluctuations and Trading activity')
plt.show()
plt.close()


average_price = []
price_variance = []
average_trading_activity = []
trading_activity_variance = []

# Generate order parameters for varying control parameter
for fundamentalist_news in Fundamentalist_news:
    news_relevance = [fundamentalist_news, 0.5]
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
plt.plot(Fundamentalist_news, average_price, color = 'purple')
plt.fill_between(Fundamentalist_news, (np.array(average_price)-ci_price), (np.array(average_price)+ci_price), color='purple', alpha=.25)
plt.ylabel('Mean price')
plt.subplot(212)
plt.plot(Fundamentalist_news, average_trading_activity, color = 'red')
plt.fill_between(Fundamentalist_news, (np.array(average_trading_activity)-ci_trading_activity), (np.array(average_trading_activity)+ci_trading_activity), color='red', alpha=.25)
plt.ylabel('Mean trading activity')
plt.xlabel('Factor of News relevance for Fundamentalists')
plt.suptitle('Emergence of Price fluctuation and Trading activity')
plt.show()
plt.close()

# Price transitions: we observe that for sensitivity > 1.1 the mean price fluctuates
# a lot more --> potentially interesting to create a confidence interval to have an area in which the mean 
# price is expected to lie

# Trading activity: for all runs so far it has been observed that the trading activity is minimal if 
# the sensitivity constant is below 0.7. Note that this aligns nicely with the results observed yesterday as well.


## MAP OF DIFFERENT REGIMES
# Regimes are minimal trading activity and increased trading activity
# initialize storage for parameters, mean prices, and trading activity
Prices_matrix = []
Trading_activity_matrix = []

# initialize fundamentalist probability variations & iterate through different probabilities
for fundamentalist_probability in Fundamentalist_news:
    news_relevance = [fundamentalist_probability, 0.5]
    # variate sensitivity constant
    Prices = []
    Trading = []
    for sensitivity_constant in sensitivity_variations:
        # initialize storage for each set of parameters and simulation results
        price_storage = []
        trading_activity_storage = []
        # simulate 30 times per parameter set for statistical significance
        for statistical_significance in range(3):
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
plt.imshow(transitions_trading_activity, extent=[min(sensitivity_variations), max(sensitivity_variations), min(Fundamentalist_news), max(Fundamentalist_news)], origin='lower', cmap='plasma_r')
plt.colorbar(label='Mean Trading Activity')
# Add labels and title
plt.xlabel('Sensitivity Constant')
plt.ylabel('News relevance for Fundamentalists')
plt.title('Phase Transition Map')
# Show the plot
plt.show()


## MAP OF DIFFERENT REGIMES FOR NEWS RELEVANCE
# Regimes are minimal trading activity and increased trading activity
# initialize storage for parameters, mean prices, and trading activity
Prices_matrix = []
Trading_activity_matrix = []

# initialize fundamentalist probability variations & iterate through different probabilities
Imitator_news = np.arange(0,1.3, 0.1)
for fundamentalist_probability in Fundamentalist_news:
    # variate sensitivity constant
    Prices = []
    Trading = []
    for imitators_probability in Imitator_news:
        news_relevance = [fundamentalist_probability, imitators_probability]
        # initialize storage for each set of parameters and simulation results
        price_storage = []
        trading_activity_storage = []
        # simulate 30 times per parameter set for statistical significance
        for statistical_significance in range(3):
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
# DEFINITIELY CROSS CHECK IF WE ARE PLOTTING THE RIGHT AXES !!!
plt.imshow(transitions_trading_activity, extent=[min(Imitator_news), max(Imitator_news), min(Fundamentalist_news), max(Fundamentalist_news)], origin='lower', cmap='plasma_r')
plt.colorbar(label='Mean Trading Activity')
# Add labels and title
plt.xlabel('News relevance for Imitators')
plt.ylabel('News relevance for Fundamentalists')
plt.title('Phase Transition Map')
# Show the plot
plt.show()


