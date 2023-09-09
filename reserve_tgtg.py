import time
import os
import pytz
import argparse
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

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--store-item-id', required=True, help="ID of the store item")
parser.add_argument('--num-items', type=int, default=1, help="Number of items to reserve")
args = parser.parse_args()

# Initialize client
client = TgtgClient(access_token=access_token, refresh_token=refresh_token, user_id=user_id, cookie=cookie)

while True:
    # Get item status
    item = client.get_item(item_id=args.store_item_id)
    item_available = item['items_available']

    next_purchase_time_utc = datetime.strptime(item['next_sales_window_purchase_start'], '%Y-%m-%dT%H:%M:%SZ')
    next_purchase_time_local = next_purchase_time_utc.replace(tzinfo=pytz.utc).astimezone(tz=None)
    time_until_next_purchase = next_purchase_time_local - datetime.now(pytz.utc).astimezone(tz=None)
    
    print(f"{get_current_timestamp()} - Next purchase time is at {next_purchase_time_local}. Time until next purchase: {time_until_next_purchase}")

    # If item is sold out, check when it was sold out
    if 'sold_out_at' in item and item['sold_out_at']:
        sold_out_at_utc = datetime.strptime(item['sold_out_at'], '%Y-%m-%dT%H:%M:%SZ')
        sold_out_at_local = sold_out_at_utc.replace(tzinfo=pytz.utc).astimezone(tz=None)  # convert UTC to local time
        if datetime.now(pytz.utc).astimezone(tz=None) - sold_out_at_local < timedelta(minutes=10): # make datetime.now() timezone aware
            print(f"{get_current_timestamp()} - Item was sold out in the last 10 minutes. Exiting...")
            break

    # If item is available, reserve it
    if item_available >= args.num_items:
        print(f"{get_current_timestamp()} - Item is available. Attempting to create order...")
        order = client.create_order(args.store_item_id, args.num_items)

        # Check order status
        order_status = client.get_order_status(order['id'])
        if order_status['state'] == 'RESERVED':
            print(f"{get_current_timestamp()} - Order created and reserved successfully, order id: {order['id']}")
            print(f"{get_current_timestamp()} - Full order details: {order}")
            break
        else:
            print(f"{get_current_timestamp()} - Failed to create order. Retrying in 500ms...")
    else:
        print(f"{get_current_timestamp()} - Item is not available. Retrying...")
    
    # Sleep for longer if it's not time for the next purchase time.
    if time_until_next_purchase.total_seconds() > 120:
        time.sleep(30)
    elif time_until_next_purchase.total_seconds() > 15:
        time.sleep(5)
    elif time_until_next_purchase.total_seconds() > 10:
        time.sleep(1)
    else:
        time.sleep(0.05)