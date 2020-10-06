# -*- coding: utf-8 -*-
""""
Created on Fri Oct  2 07:50:48 2020
Automated Strategy- BTC ACCUMULATOR

@author: - Grant DePalma
"""
# Initial Imports
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import shrimpy
from joblib import dump, load
import time

# Set environment variables from the .env file
env_path = Path("/Users/gdepa")/'grant_api_keys.env'
load_dotenv(env_path)
shrimpy_public_key = os.getenv("SHRIMPY_DEV_PUBLIC")
shrimpy_private_key = os.getenv("SHRIMPY_DEV_SECRET")
shrimpy_client = shrimpy.ShrimpyApiClient(shrimpy_public_key, shrimpy_private_key)    
KRAKEN_API_KEY = os.getenv("KRAKEN_API_KEY")
KRAKEN_PRIVATE_KEY = os.getenv("KRAKEN_PRIVATE_KEY")
users = shrimpy_client.list_users()
shrimpy_user_id = users[1]['id'] # first id in list of users
kraken_id = 39593

def fetch_data():
    # Set environment variables from the .env file
    env_path = Path("/Users/gdepa")/'grant_api_keys.env'
    load_dotenv(env_path)
    shrimpy_public_key = os.getenv("SHRIMPY_DEV_PUBLIC")
    shrimpy_private_key = os.getenv("SHRIMPY_DEV_SECRET")
    shrimpy_client = shrimpy.ShrimpyApiClient(shrimpy_public_key, shrimpy_private_key)   
    users = shrimpy_client.list_users()
    shrimpy_user_id = users[1]['id'] # first id in list of users
    kraken_id = 39593
# Retrieve Balance Information From Shrimpy Rest API
    balance = shrimpy_client.get_balance(shrimpy_user_id, kraken_id)
    holdings = balance['balances']
    asset_balances = []
    asset_values_usd = []
    asset_values_btc = []
    symbols = []
    
    # This is a sample handler, it simply prints the incoming message to the console
    def error_handler(err):
        print(err)
    
    # Create the websocket client - set up socket communication
    #api_client = shrimpy.ShrimpyApiClient(shrimpy_public_key, shrimpy_private_key)
    #raw_token = api_client.get_token()
    #ws_client = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])
    
    # collect asset balances on the exchange
    balance = shrimpy_client.get_balance(shrimpy_user_id, kraken_id)
    holdings = balance['balances']
    asset_balances = []
    asset_values_usd = []
    asset_values_btc = []
    symbols = []
    for asset in holdings:
        asset_symbol = asset['symbol']
        asset_amount = asset['nativeValue']
        asset_value_usd = asset['usdValue']
        asset_value_btc = asset['btcValue']
        asset_balances.append(asset_amount)
        asset_values_usd.append(asset_value_usd)
        asset_values_btc.append(asset_value_btc)
        symbols.append(asset_symbol)
    
        balances_df = pd.DataFrame(columns = ['symbol','asset_balance','usd_balance', 'btc_balance', 'wt_of_total_usd', 'wt_of_total_btc'])
        balances_df['symbol'] = symbols
        balances_df['asset_balance'] = asset_balances
        balances_df['usd_balance'] = asset_values_usd
        balances_df['btc_balance'] = asset_values_btc
        # Save balances to dataframe
    balances_df = pd.DataFrame(columns = ['symbol','asset_balance','usd_balance', 'btc_balance', 'wt_of_total_usd', 'wt_of_total_btc'])
    balances_df['symbol'] = symbols
    balances_df['asset_balance'] = asset_balances
    balances_df['usd_balance'] = asset_values_usd
    balances_df['btc_balance'] = asset_values_btc
    total_balance_usd = balances_df['usd_balance'].sum()
    total_balance_btc = balances_df['btc_balance'].sum()
    balances_df['wt_of_total_usd'] = balances_df['usd_balance']/total_balance_usd
    balances_df['wt_of_total_btc'] = balances_df['btc_balance']/total_balance_btc
    
    # retrieve Price Data
    exchange = 'kraken'
    universe_assets = ['XBT', 'USD', 'ETH']
    quote_currencies = ['XBT', 'USD']
    interval = '6h'
    start = '2018-01-01' # 1000 candle limit
    # Get and organize closing prices into dataframe from list of trading pairs from one exchange from shrimpy rest api
    def calc_trading_pairs_df(exchange):
        exchange_pairs = shrimpy_client.get_trading_pairs(exchange)
        exchange_pairs_df = pd.DataFrame(columns=['base','quote'])
        for key, value in enumerate(exchange_pairs):
            exchange_pairs_df.loc[key] = [value['baseTradingSymbol'],value['quoteTradingSymbol']]
        return exchange_pairs_df
    
    def universe_selection(universe_assets, quote_currencies):
        trading_pairs_df = calc_trading_pairs_df
        universe_pairs_df = trading_pairs_df[(trading_pairs_df['base'].isin(universe_assets) & trading_pairs_df['quote'].isin(quote_currencies))]
        return universe_pairs_df
    
    def get_universe_prices(exchange, universe_pairs_df, interval, start):
        universe_prices_df = pd.DataFrame()
        for index, row in universe_pairs_df.iterrows():
            candles = shrimpy_client.get_candles(exchange, row['base'], row['quote'], interval, start)
            time = []
            prices = []
            for key, value in enumerate(candles):
                time.append(value['time'])
                prices.append(value['close'])
            prices_df = pd.DataFrame(list(zip(time, prices)), columns = ['time', row['base'] + "_" + row['quote']])
            prices_df['time'] = pd.to_datetime(prices_df['time'])
            if universe_prices_df.empty:
                universe_prices_df = prices_df
            else:
                universe_prices_df = pd.merge(universe_prices_df, prices_df, left_on='time', right_on = 'time', how = 'left')
        return universe_prices_df 

    universe_pairs_df=universe_selection(universe_assets,quote_currencies)
    universe_prices_df = get_universe_prices(exchange, universe_pairs_df, interval, start)
    return universe_prices_df, balances_df

# make sure rows are every 6hrs, if there is no row-then make one and forward fill data (shrimpy doesn't print candle if there is no tick)
def calc_feature_df(prices_df):
    ## cumulative returns as velocity
    ## Log returns as velocity
    ## partials?
    ## Lags?
    ## stock to flow
    ## Technical Indicators
    ## Social Indicators

    df_features = prices_df
    # Construct dependent variable
    df_features['returns'] = df_features['close'].pct_change()
    # Calculate cumulative returns
    df_features['cum_returns'] = (df_features['returns']+1).cumprod()
    # ----------------------- Price Dynamics --------------------------------
    # price dynamics as a one Dimensional particle problem in physics
    df_features['price_velocity_2'] = df_features['close'].pct_change(2)
    df_features['price_velocity_3'] = df_features['close'].pct_change(3)
    df_features['price_velocity_4'] = df_features['close'].pct_change(4)
    df_features['price_velocity_7'] = df_features['close'].pct_change(7)
    df_features['price_velocity_30'] = df_features['close'].pct_change(30)
    
    df_features['price_acceleration_1'] = df_features['returns'].pct_change(1)
    df_features['price_acceleration_2'] = df_features['price_velocity_2'].pct_change(2)
    df_features['price_acceleration_3'] = df_features['price_velocity_3'].pct_change(3)
    df_features['price_acceleration_4'] = df_features['price_velocity_4'].pct_change(4)
    df_features['price_acceleration_7'] = df_features['price_velocity_7'].pct_change(7)
    df_features['price_acceleration_30'] = df_features['price_velocity_30'].pct_change(30)

    df_features['rolling_mean_velocity_2'] = df_features['returns'].rolling(window=2).mean()
    df_features['rolling_mean_velocity_3'] = df_features['returns'].rolling(window=3).mean()
    df_features['rolling_mean_velocity_4'] = df_features['returns'].rolling(window=4).mean()
    df_features['rolling_mean_velocity_7'] = df_features['returns'].rolling(window=7).mean()
    df_features['rolling_mean_velocity_30'] = df_features['returns'].rolling(window=30).mean()
    
    df_features['rolling_mean_acceleration_2'] = df_features['price_acceleration_1'].rolling(window=2).mean()
    df_features['rolling_mean_acceleration_3'] = df_features['price_acceleration_1'].rolling(window=3).mean()
    df_features['rolling_mean_acceleration_4'] = df_features['price_acceleration_1'].rolling(window=4).mean()
    df_features['rolling_mean_acceleration_7'] = df_features['price_acceleration_1'].rolling(window=7).mean()
    df_features['rolling_mean_acceleration_30'] = df_features['price_acceleration_1'].rolling(window=30).mean()
    # To extend space to entire line the log price is mapped to position x(t) in the space by
    # x(t) = log(S(t))   where S(t) is the price of the instrument
    df_features['log_price'] = np.log(df_features['close'])
    df_features['log_returns'] = df_features['log_price'].diff() # Diff or percent change
    #df_features['log_return_pct']  = df_features['log_price'].pct()
    #df_features['cum_log_returns'] =(df_features['log_returns_pct'] + 1).cumprod()
    # Assumption: Returns of financial instruments are lognormally distributed
    # v(t) = R(t) = dx(t)/dt where v(t) is the velocity of the instrument in the log price space, x(t)
    
    # ------------------------------ partial price dynamics ---------------------
    # -------------------------------Technical Indicators ------------------------
    df_features.dropna(inplace=True)
    return df_features


def load_model(features_df):
    X_test = features_df.drop(columns=["XBT_USD", "returns","cum_returns"])
    nameOfModel = 'XG BOOST CLASSIFIER'
    model = load(r'C:\Users\gdepa\finalized_model.joblib')
    y_pred = model.predict(X_test)
    predictions = y_pred.reshape(-1,1)
    predictions_df = pd.DataFrame({"Predicted": predictions.ravel()})
    return predictions_df

#------------------ Automated Strategy -------------------------
# Set up data for Model
balances_df, universe_prices_df = fetch_data()
features_df = calc_feature_df(universe_prices_df)
predictions_df = load_model(features_df)

# Set Global Variables
#symbol = ['xbtusd']
bar = '6h'
btc_threshold =  .6
position = 0
vbull_wt = .2 #80% ethereum
neutral_wt = 1

# check in Jupyter Lab
btc_balances_df = balances_df[balances_df['symbol']=='XBT']
current_btc_wt = btc_balances_df['wt_of_total_btc'][0]

# min_bars = lags + 1
# df = pd.DataFrame()

#def generate_profits(balances_df):           
def btc_accumulator(predictions_df):#(freq=6, threshold=.6):
    if predictions_df['predicted'] == 1:
        wt_optimized = vbull_wt
    if predictions_df['predicted'] == 0:
        wt_optimized = neutral_wt        
    # Calculate current balances
    usd_balance = balances_df[balances_df['symbol']=='USD']['usd_balance'].sum()
    xbt_balance = balances_df[balances_df['symbol']=='XBT']['usd_balance'].sum()
    alt_balances_df = balances_df[balances_df['symbol']!='USD']
    alt_balances_df = alt_balances_df[alt_balances_df['symbol']!='XBT']
    alt_balance = balances_df['usd_balance'].sum()
    trading_balance_wt = usd_balance + alt_balance
    # Allocation Logic
    if trading_balance_wt > 1-btc_threshold: # if trading balance weight is greater than .4 collect profits
        btc_wt = btc_threshold # accumulating bitcoin from trading profits
        usd_wt = (1-btc_threshold)*(wt_optimized) # allocating .4(1- optimized eth wt)
        eth_wt = (1-btc_threshold)*(1-wt_optimized) #  allocating .4 (optimized eth wt)
    else:
        btc_wt = current_btc_wt
        usd_wt = (1-current_btc_wt)*wt_optimized-1
        eth_wt = (1-current_btc_wt)*wt_optimized
    meta_level_wts = [btc_wt, usd_wt, eth_wt]
    return meta_level_wts

meta_level_wts = btc_accumulator()

              
def rebalancePortfolio(meta_level_wts, account_id, user_id):
    shrimpy_client.set_strategy(user_id, account_id, {
        "isDynamic":False,
        "allocations": [
            {"symbol": "XBT", "percent": meta_level_wts[0]},
            {"symbol": "USD", "percent": meta_level_wts[1]},
            {"symbol": "ETH", "percent": meta_level_wts[2]}
        ]               
    })
    shrimpy_client.rebalance(user_id, account_id) # rebalancing to strategy weights
    
    
# LOGGING FUNCTIONS
# ALERT FUNCTIONS

    


    