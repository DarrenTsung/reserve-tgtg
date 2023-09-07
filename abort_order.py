import time
import os
import pytz
import argparse
from tgtg import TgtgClient
from datetime import datetime
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

# Initialize argument parser
parser = argparse.ArgumentParser(description='Abort order.')
parser.add_argument('--order-id', type=str, help='Order ID to abort', required=True)
args = parser.parse_args()

# Initialize client
client = TgtgClient(access_token=access_token, refresh_token=refresh_token, user_id=user_id, cookie=cookie)

# Check order status
order_status = client.get_order_status(args.order_id)
print(f"{get_current_timestamp()} - Order {args.order_id} status: {order_status['state']}")

# If the order is in a state that can be aborted, abort it.
if order_status['state'] == 'RESERVED':
    client.abort_order(args.order_id)
    print(f"{get_current_timestamp()} - Order {args.order_id} has been successfully aborted.")
else:
    print(f"{get_current_timestamp()} - Order {args.order_id} is not in a state that can be aborted.")