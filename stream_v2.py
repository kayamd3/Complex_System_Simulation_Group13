
import streamlit as st
import numpy as np
import tempfile
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import Functions
import time 

# Initialize Streamlit app
st.title("Cellular Automata Market Simulation")

# Initialize session_state
if 'timestep' not in st.session_state:
    st.session_state.timestep = 0

# Sidebar for parameters
st.sidebar.title("Simulation Parameters")
fundamentalist_ratio = st.sidebar.slider("Imitator Ratio", 0.0, 1.0, 0.3, 0.01)
sensitivity_constant = st.sidebar.slider("Sensitivity Constant", 0.0, 1.0, 0.8, 0.01)
time_steps = st.sidebar.slider('Time Steps', min_value=10, max_value=500, value=100)
fundamental_value = st.sidebar.number_input('Fundamental Value', min_value=1, value=100)
initial_price = st.sidebar.number_input('Initial Price', min_value=1, value=100)
grid_size = st.sidebar.number_input('Grid Size (L)', min_value=1, value=10)

plot_choice = st.sidebar.radio("Select Plot to Display", ("Cellular Automata", "Price vs Time"))

L = grid_size
trader_grid = Functions.grid_stock_market(L, fundamentalist_ratio)
fundamental_value = 100
initial_price = initial_price
time_steps = time_steps
sensitivity_constant = sensitivity_constant
constant_trading = 20
news_relevance = [0.2, 0.7]
stock_favorability = 0.01
period_length = 10
threshold = 0.0001

# Placeholders for plots and percentages
placeholder_ca = st.empty()
placeholder_price = st.empty()
placeholder_percentages = st.empty()

def Level_3_simulation(trader_grid, initial_price, fundamental_value, time, L, sensitivity_constant, constant_trading, news_relevance, stock_favorability, period_length):
    """
        Parameters:
        Uses the same parameters as stated in level 1 plus some extra
        - constant_trading (float): A constant representing the base level of trading activity in the market.
        - news_relevance (float): A measure of how relevant news is to the market, influencing traders' decisions.
        - stock_favorability (float): A measure of the overall favorability of the stock among traders.
        - period_length (int): The length of the period over which price fluctuations are considered.


        Returns:
        - tuple: A tuple containing four lists:
            - transactions (list of numpy.ndarray): A list of arrays representing the transaction quantities at each time step.
            - price_list (list of float): A list of stock prices at each time step.
            - price_fluctuation_list (list of float): A list of price fluctuations at each period.
            - trades_list (list of float): A list of trading activity levels at each time step.

    """
    
    price_list = [initial_price]
    price_fluctuation = Functions.price_fluctuations(period_length, price_list)
    price_fluctuation_list = [price_fluctuation]
    trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
    trades_list = [trades]
    
    transaction_quantities, news_both = Functions.next_state_Level_3(trader_grid, np.zeros((L, L)), price_list, fundamental_value, news_relevance, L, trades)
    transactions = [transaction_quantities]
    
    for t in range(time):
        price_fluctuation = Functions.price_fluctuations(period_length, price_list)
        price_fluctuation_list.append(price_fluctuation)
        trades = Functions.trading_activity_function(constant_trading, price_fluctuation, stock_favorability)
        trades_list.append(trades)
        
        transaction_quantities, _ = Functions.next_state_Level_3(trader_grid, transactions[-1], price_list, fundamental_value, news_relevance, L, trades)
        transactions.append(transaction_quantities)
        
        trans_quantity = Functions.calculation_transaction_quantity(transaction_quantities, L)
        price_list.append(Functions.price_function(price_list[-1], sensitivity_constant, L, trans_quantity))
    
    return transactions, price_list, price_fluctuation_list, trades_list


fundamentalist_counts = {'buy': 0, 'hold': 0, 'sell': 0}
imitator_counts = {'buy': 0, 'hold': 0, 'sell': 0}


def process_transactions(transactions, trader_grid, price_list, fundamental_value, L):
    processed = np.zeros_like(transactions, dtype=int)
    
    for t in range(transactions.shape[0]):
        for i in range(L):
            for j in range(L):
                trader_type = 1 if trader_grid[i, j] == 1 else 4  # 1 for Fundamentalist, 4 for Imitator
                current_price = price_list[t]
                action = 1  # Default action is holding

                if trader_type == 1:  # Fundamentalist
                    if current_price < fundamental_value:  # Buy when price is below fundamental value
                        action = 2  # Buying
                    elif current_price > fundamental_value:  # Sell when price is above fundamental value
                        action = 0  # Selling

                else:  # Imitator
                    neighborhood = transactions[t, max(0, i-1):min(L, i+2), max(0, j-1):min(L, j+2)]
                    avg_action = np.mean(neighborhood)
                    if avg_action > threshold:  # Define a threshold for buying
                        action = 2  # Buying
                    elif avg_action < -threshold:  # Define a threshold for selling
                        action = 0  # Selling
                    else:
                        action = 1  # Holding


                processed[t, i, j] = trader_type + action

    return processed

# Function to save plots as images
def save_plot_ca_only(processed_transactions, timestep, trader_grid, L):
    # Create a figure for CA grid plot
    fig, ax_ca = plt.subplots(figsize=(15, 15))  # Adjust figsize for CA grid size

    # Cellular Automata Grid Plot
    cmap = ListedColormap(['darkred', 'lightcoral', 'red', 'darkblue', 'lightblue', 'blue'])
    norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], cmap.N)
    mat = ax_ca.imshow(processed_transactions[timestep], cmap=cmap, norm=norm)
    for i in range(L):
        for j in range(L):
            text = 'F' if trader_grid[i, j] == 1 else 'I'
            ax_ca.text(j, i, text, ha='center', va='center', color='white', fontsize=21)
    colorbar = fig.colorbar(mat, ax=ax_ca, cmap=cmap, norm=norm, boundaries=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], ticks=[1, 2, 3, 4, 5, 6])
    colorbar.ax.set_yticklabels(['F Selling', 'F Holding', 'F Buying', 'I Selling', 'I Holding', 'I Buying'], fontsize=22)
    ax_ca.set_title(f'CA Grid - Timestep: {timestep},  Price: {current_price:.2f}', fontsize=28)
    ax_ca.tick_params(axis='both', labelsize=24)


    # Save the figure as an image and return the file path
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight')
        plt.close(fig)
    return tmpfile.name

def save_plot_price_only(price_list, timestep):
    # Create a figure for the Price vs Time plot
    fig, ax_price = plt.subplots(figsize=(20, 15))  # Adjust figsize as needed

    # Plotting the stock price over time
    ax_price.plot(price_list[:timestep + 1], color='blue')
    ax_price.set_title(f'Stock Price - Timestep: {timestep},  Price: {current_price:.2f}', fontsize=28)
    ax_price.set_xlabel('Time', fontsize=28)
    ax_price.set_ylabel('Price', fontsize=28)
    ax_price.tick_params(axis='both', labelsize=24)


    # Save the figure as an image and return the file path
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        fig.savefig(tmpfile.name, bbox_inches='tight')
        plt.close(fig)
    return tmpfile.name

# Function to calculate and format action statistics as percentages
def calculate_action_statistics_percentage():
    total_count = max(fundamentalist_counts['buy'] + fundamentalist_counts['hold'] + fundamentalist_counts['sell'] +  imitator_counts['buy'] + imitator_counts['hold'] + imitator_counts['sell'],1)

    # Calculate the counts as percentages
    fundamentalists_bought = round((fundamentalist_counts['buy'] / total_count) * 100, 2)
    fundamentalists_sold = round((fundamentalist_counts['sell'] / total_count) * 100, 2)
    fundamentalists_held = round((fundamentalist_counts['hold'] / total_count) * 100, 2)
    
    imitators_bought = round((imitator_counts['buy'] / total_count) * 100, 2)
    imitators_sold = round((imitator_counts['sell'] / total_count) * 100, 2)
    imitators_held = round((imitator_counts['hold'] / total_count) * 100, 2)
    
    action_statistics_percentage = {
        "Fundamentalists bought (%)": fundamentalists_bought,
        "Fundamentalists sold (%)": fundamentalists_sold,
        "Fundamentalists held (%)": fundamentalists_held,
        "Imitators bought (%)": imitators_bought,
        "Imitators sold (%)": imitators_sold,
        "Imitators held (%)": imitators_held
    }
    
    return action_statistics_percentage

# Function to display action statistics
def display_action_statistics_popup(action_statistics):
    st.info("Action Statistics as Percentages:")
    for key, value in action_statistics.items():
        st.write(f"{key}: {value:.2f}%")

# Run simulation and display images on button click
if st.sidebar.button('Run Simulation'):
    # Create a single placeholder for the image
    image_placeholder = st.empty()

    for t in range(time_steps):  
        # Run simulation for one timestep
        transactions, price_list, _, _ = Level_3_simulation(
            trader_grid, initial_price, fundamental_value, time_steps, grid_size, 
            sensitivity_constant, constant_trading, news_relevance, 
            0.01, 10
        )
        transactions_array = np.array(transactions)
        processed_transactions = process_transactions(transactions_array, trader_grid, price_list, fundamental_value, L)
        current_price = price_list[t] 
        if plot_choice == "Cellular Automata":
            # Save and display CA plot for the current timestep
            image_path = save_plot_ca_only(processed_transactions, t, trader_grid, grid_size)
        else:
            # Save and display Price vs Time plot for the current timestep
            image_path = save_plot_price_only(price_list, t)  # You need to define this function

        image_placeholder.image(image_path, use_column_width=True)
        
        # Calculate and update action counts
        action_statistics = calculate_action_statistics_percentage()

        # Remove the saved image file after displaying
        os.remove(image_path)
        time.sleep(0.1)  # Control the speed of animation

    # Display action statistics at the end of the simulation as percentages
    display_action_statistics_popup(action_statistics)
