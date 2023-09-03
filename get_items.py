# Use this script to list your favorite items to get the item ids.

import time
import os
from tgtg import TgtgClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
access_token = os.getenv('TGTG_ACCESS_TOKEN')
refresh_token = os.getenv('TGTG_REFRESH_TOKEN')
user_id = os.getenv('TGTG_USER_ID')
cookie = os.getenv('TGTG_COOKIE')

client = TgtgClient(access_token=access_token, refresh_token=refresh_token, user_id=user_id, cookie=cookie)
print(client.get_items())