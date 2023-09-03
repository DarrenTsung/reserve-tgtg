import time
import argparse
from tgtg import TgtgClient
from datetime import datetime

parser = argparse.ArgumentParser(description='Get credentials')
parser.add_argument('--email', required=True, help='Email')

# Parse arguments
args = parser.parse_args()

client = TgtgClient(email=args.email)
print(f'Requesting credentials, please check your email and validate the login attempt!')
credentials = client.get_credentials()
print(credentials)