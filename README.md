# Mantis Trading

## What is Mantis Trading? 

Mantis Trading is a mock trading firm that uses algorithmic trading to accumulate Bitcoin, with a focus on cryptocurrencies built by the students, TA's, and Class Instructor during the 2020 Northwestern Fintech Bootcamp. 

### Team
* Grant DePalma
* Dave Rea
* Scott Andersen
* Reuben Lopez
* Javier Mendez

### Files in this Repository

#### In the mantis-trading folder, you may find the following files:
* **initialize.py**: Initializes the trading and pulls API keys. 
* **df_candles_kraken_btcusd_6h_append_9102.csv**: Data used to train the model in mantis.py
* **mantis.py**: Prediction software. This is the algorythm used that determines the investment strategy for any given moment. 
* **strategy.py**: Trading software. Executes the trading strategy on Kraken or any other exchange.
* **monitor.py**: Performance software. Used to monitor the peformance of the algorythm through the use of visuals.

#### In the resources folder, you may find the following files:
* **resources.md**: Markdown file containing useful links to the resources used to create this project. 

### Major Assumptions
* When Bitcoin is in a bull market, altcoins outperform Bitcoin relative to the USD
* When Bitcoin is in a bear market, altcoins underperform 
* SHRIMPY DEVELOPER API can Scale with our ALGORITHMIC TRADING APPLICATION
* Momentum strategies are more successful than mean reversion in the crypto markets
* Measuring OHLCV instead of tick-data is efficient for rolling calculus measurements

## How does Mantis Trading predict Bitcoin's performance?

## Services used to get Mantis running
* **Shrimpy Developers**: "Universal Crypto Exchange Trading API. The industry leading API for crypto trading, real-time data collection, and exchange account management. Execute trades across thousands of markets on every major exchange by taking advantage of the Shrimpy low latency execution endpoints for crypto trading." We used Shrimpy Developers to obtain Bitcoin and Altcoin historical data, retrieve real time information, and to execute live trading strategies across multiple Crypto Exchanges.
* **Kraken**: "Kraken is a US-based cryptocurrency exchange, founded in 2011. The exchange provides cryptocurrency to fiat trading, and provides price information to Bloomberg Terminal. As of 2020, Kraken is available to residents of 48 U.S. states and 176 countries, and lists 40 cryptocurrencies available for trade." We linked Kraken to the Shimpy Developer API to execute our trades from Mantis algorithm. 
* **JupyterLab**: "JupyterLab is a web-based interactive development environment for Jupyter notebooks, code, and data. JupyterLab is flexible: configure and arrange the user interface to support a wide range of workflows in data science, scientific computing, and machine learning." We used JupyterLab to do research, backtest, and create our live trading functionality.
* **Spyder**: Spyder is an open source cross-platform integrated development environment (IDE) for scientific programming in the Python language. We used for de-bugging and executing our software programs.
