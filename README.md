# reserve-tgtg

Script to help reserve an item on "Too Good To Go" via the unofficial python client.

## How to use

First, install the pre-requisite libraries:

```
pip install tgtg
pip install python-dotenv
pip install pytz
```

Get your credentials via the `get_credentials.py` script (requires clicking a login link in your email):

```
python get_credentials.py --email YOUR_EMAIL_HERE
```

Then create a .env file in this repository that looks like the following, filling out the placeholders with the credentials you got from the script:

```
TGTG_ACCESS_TOKEN="..."
TGTG_REFRESH_TOKEN="..."
TGTG_USER_ID=...
TGTG_COOKIE="..."

# To be filled out after get the item id of the item you're trying to reserve.
# TGTG_STORE_ITEM_ID=...
```

Then you can use the `get_favorite_items.py` to list all of your favorite items. The script reads the .env file to initialize the client with the correct credentials.

```
python get_favorite_items.py
```

Find the order_id of the item you're trying to reserve and place it in the .env:

```
TGTG_STORE_ITEM_ID=...
```

Then you can call the `reserve_tgtg.py` script:

```
python reserve_tgtg.py
```

The script will check the item status and attempt to reserve it every 500ms. Note that the unofficial python API does not support paying for the order, so the order will only be reserved and will stay reserved for up to 5 minutes.

My strategy is to wait a period of time (2-3 minutes), open up the TGTG app, and then use the `abort_order.py` script to abort the reserved order. Then immediately open the store in the app and reserve and pay for the item.

```
python abort_order.py --order-id YOUR_ORDER_ID
```
