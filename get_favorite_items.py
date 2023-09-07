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
favorite_items = client.get_items()
for favorite_item in favorite_items:
	print({
		'item_id': favorite_item['item']['item_id'],
		'description': favorite_item['item']['description'],
		'item_category': favorite_item['item']['item_category'],
		'store_name': favorite_item['store']['store_name'],
	})
