# Complex System Simulation - Examine Volatility Clustering in a Stock Market using CA
# Group 13
  Group members : K. M. Disselkamp, F. Catania, P. Venkatesh, Y. Lu

## Project Task Assignments

| Responsible Person | Task |
|--------------------|-------------------|
| K. M. Disselkamp   | Create Baseline/Expanded model function + Phase transition Diagrams
| F. Catania         | Examine stylized facts obtained from Expanded model + Parameter sweep for Fundamentalist Ratio
| P. Venkatesh       | CA Animations + Streamlit visualisation. Heatmaps for Mean-Variance in Price
| Y. Lu              | Garch Model Analysis + Network Model Analysis

## Overview
Our aim for this project was to examine emergence properties in a stock market. We did so by using a simplified model (Cellular Automata) in order to model complex dynamics in a Stock Market.
We first created a Baseline model and found no emergence properties as it came to an equilibrium point. To expand the model, we incorporated stochasticity in the form of news.
This was the basis for our Expanded model. Both of which are found in the notebook: CA and the stock market - results.

If you'd like to have a play around with the parameters on the Expanded model please run the stream_v2.py file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

```bash
git clone https://github.com/koenweverink/stochastic_simulation_assignment_2.git
cd Complex_System_Simulation_Group13
pip install -r requirements.txt
```

## Usage

- Open CA and the stock market - results.ipynb
- Select a Python interpreter
- Press run all 

Please keep in mind it will take quite some time for it to run entirely. To speed up the process, you may need to reduce the grid size (L) and timesteps (from 500 to 100). 
You may also need to reduce the number of simulations it does from 30 to, say, 5.
