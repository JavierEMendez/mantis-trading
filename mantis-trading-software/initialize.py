# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:20:52 2020

@author: - mantis
"""
# Initial Imports
from pathlib import Path
from dotenv import load_dotenv
import os
import shrimpy

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

# ----------------- LINK Exchanges to SHRIMPY(SHA256) --------------------
# LINK Kraken exchange (hard code)
kraken_account_response = shrimpy_client.link_account(shrimpy_user_id,
                                           'kraken',
                                           KRAKEN_API_KEY,
                                           KRAKEN_PRIVATE_KEY)
kraken_id = kraken_account_response['id']
print(kraken_id)

