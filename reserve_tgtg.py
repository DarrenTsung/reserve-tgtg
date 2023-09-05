import time
import os
import pytz
from tgtg import TgtgClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

# Load environment variables from .env file
load_dotenv()

# Get environment variables
access_token = os.getenv('TGTG_ACCESS_TOKEN')
refresh_token = os.getenv('TGTG_REFRESH_TOKEN')
user_id = os.getenv('TGTG_USER_ID')
cookie = os.getenv('TGTG_COOKIE')
store_item_id = os.getenv('TGTG_STORE_ITEM_ID')

# Initialize client
client = TgtgClient(access_token=access_token, refresh_token=refresh_token, user_id=user_id, cookie=cookie)

while True:
    # Get item status
    item = client.get_item(item_id=store_item_id)
    item_available = item['items_available']

    # If item is sold out, check when it was sold out
    if 'sold_out_at' in item and item['sold_out_at']:
        sold_out_at_utc = datetime.strptime(item['sold_out_at'], '%Y-%m-%dT%H:%M:%SZ')
        sold_out_at_local = sold_out_at_utc.replace(tzinfo=pytz.utc).astimezone(tz=None)  # convert UTC to local time
        if datetime.now(pytz.utc).astimezone(tz=None) - sold_out_at_local < timedelta(minutes=10): # make datetime.now() timezone aware
            print(f"{get_current_timestamp()} - Item was sold out in the last 10 minutes. Exiting...")
            break

    # If item is available, reserve it
    if item_available > 0:
        print(f"{get_current_timestamp()} - Item is available. Attempting to create order...")
        order = client.create_order(store_item_id, 1)

        # Check order status
        order_status = client.get_order_status(order['id'])
        if order_status['state'] == 'RESERVED':
            print(f"{get_current_timestamp()} - Order created and reserved successfully: {order}")
            break
        else:
            print(f"{get_current_timestamp()} - Failed to create order. Retrying in 500ms...")
    else:
        print(f"{get_current_timestamp()} - Item is not available. Retrying in 500ms...")

    time.sleep(0.5)