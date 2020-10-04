# Mantis Trading

## What is Mantis Trading? 

Mantis Trading is a trading firm that uses algorythmic trading to accumulate cryptocurrencies, with a focus on Bitcoin. 

### Team
* Grant DePalma
* Dave Rea
* Scott Andersen
* Reuben Lopez
* Javier Mendez

### Files in this Repository

##### In the mantis-trading folder, you may find the following files:
* **initialize.py**: Initializes the trading and pulls API keys. 
* **df_candles_kraken_btcusd_6h_append_9102.csv**: Data used to train the model in mantis.py
* **mantis.py**: Prediction software. This is the algorythm used that determines the investment strategy for any given moment. 
* **strategy.py**: Trading software. Executes the trading strategy on Kraken or any other exchange.
* **monitor.py**: Performance softwarte. Used to monitor the peformance of the algorythm through the use of visuals.

##### In the resources folder, you may find the following files:
* **resources.md**: Markdown file containing useful links to the resources used to create this project. 

### Major Assumptions
* When Bitcoin is in a bull market, altcoins outperform Bitcoin relative to the USD
* When Bitcoin is in a bear market, altcoins underperform 
* SHRIMPY DEVELOPER API can Scale with our ALGORITHMIC TRADING APPLICATION
* Momentum strategies are more successful than mean reversion in the crypto markets
* Measuring OHLCV instead of tick-data is efficient for rolling calculus measurements

## How does Mantis Trading predict Bitcoin's performance?

## Services used to get Mantis running
* **Shrimpy**: API used to obtain Bitcoin and Altcoin data.
* **Kraken**: Exchange linked to be able to trade the Mantis algorythm. 
* **JupyterLab**: Used to do research, backtest, and create the LiveTrader function.
* **Spyder**: Used for general troubleshooting, research, backtesting, and creating the LiveTrader function.
