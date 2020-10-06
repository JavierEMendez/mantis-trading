""""
Created on Fri Oct  2 07:50:48 2020
Websocket Monitor

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

# This is a sample handler, it simply prints the incoming message to the console
def error_handler(err):
    print(err)

# Create the websocket client - set up socket communication
api_client = shrimpy.ShrimpyApiClient(shrimpy_public_key, shrimpy_private_key)
raw_token = api_client.get_token()
ws_client = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])


# Wait while Shrimpy collects data for the exchange account
# Only required the first time linking
time.sleep(5)

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
    # Save balances to database as multi-factor dataframe
    
balances_df = pd.DataFrame(columns = ['symbol','asset_balance','usd_balance', 'btc_balance', 'wt_of_total_usd', 'wt_of_total_btc'])
balances_df['symbol'] = symbols
balances_df['asset_balance'] = asset_balances
balances_df['usd_balance'] = asset_values_usd
balances_df['btc_balance'] = asset_values_btc
total_balance_usd = balances_df['usd_balance'].sum()
total_balance_btc = balances_df['btc_balance'].sum()

balances_df['wt_of_total_usd'] = balances_df['usd_balance']/total_balance_usd
balances_df['wt_of_total_btc'] = balances_df['btc_balance']/total_balance_btc
# calculate and print balances for each asset. 

print(f"---------------- Global Porfolio Stats ----------------------")
print(f"Total AUM (USD): {round(total_balance_usd,2)} USD")
print(f"Total AUM (BTC): {total_balance_btc} BTC")
print()
print(f"--------------- Asset Balance Stats -------------------------")
for index,row in balances_df.iterrows():
    print(f"  {row['symbol']}:  {round(row['usd_balance'],2)} USD,  {row['btc_balance']} BTC,  {round(row['wt_of_total_btc'],2)*100} %")


# Pie Chart Visualization Function
def plot_pies(balances_df):
    labels = []
    sizes = []
    for index,row in balances_df.iterrows():
        labels.append(row['symbol'])
        sizes.append(row['wt_of_total_usd'])
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,autopct= '%1.1f%%', startangle=90)
    ax1.axis('equal')
    plt.show()
plot_pies(balances_df)       
# Polar Visualization Function
def plot_polars(account_historical_df):
    # Polar Chart Visual
    radial_fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(polar="True")
    
    # define categories
    N=7
    categories = ['M', 'T', 'W', 'R', 'F', 'Sa', 'Su']
    
    # NEED TO LOAD HISTORICAL_RETURNS
    # Loop through the number of weeks in the df
    #for idx in range(len(historical_returns)):
    # get values from df and calculate angles
        #balances = account_historical_df['total_balance_btc'].iloc[idx].values.tolist()
        #cum_returns = account_historical_df['cum_returns'].iloc[idx].values.tolist()
    # Plot Balance Radial
    # Plot Cum-Returns Radial
    
def plot_timeseries(account_historical_df):
    # Plot Cumulative Returns by week
    return
 
# This is a sample handler, it simply prints the incoming message to the console
def error_handler(err):
    print(err)

# This is a sample handler, it simply prints the incoming message to the console
#def handler(msg):
    #price = msg['content'][0]['price']
    #print(btcAmount)


# Subscribe to Kraken Messages 
        
#subscribe_data = {
  #  "type": "subscribe",
   # "exchange": "kraken",
   # "pair": "xbt-usd",
   # "channel": "trade"
#}

# Start processing the Shrimpy websocket stream!
#ws_client.connect()
#ws_client.subscribe(subscribe_data, '')

#while True:
#    msg = ws_client.recv_string()
#    print(msg)