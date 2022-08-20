import pandas as pd
import numpy as np

'''
    This file is to keep all the 'private' functions used in the uniform_pricing.py file.
'''

TICK = 0.1

# takes a trade from queue and spits out a pandas DataFrame by converting it into a row in the limit order book
def generate_new_orderbook_row(trade: list) -> pd.DataFrame:
    if len(trade) != 5:
        raise Exception("Please enter a valid trade!")
    append_dict = {
        "Selling Trader": trade[0] if trade[1] == "Sell" else None,
        "Selling Size": trade[2] if trade[1] == "Sell" else None,
        "Order Price": trade[4],
        "Buying Size": trade[2] if trade[1] == "Buy" else None,
        "Buying Trader": trade[0] if trade[1] == "Buy" else None
    }
    return pd.DataFrame(append_dict, index=[0])

# finds the index of where to append a trade row into the limit order book
def find_index_to_update(data: pd.DataFrame, trade: list) -> int:
    if trade[1] == "Sell":
        for row in range(len(data) - 1, -1, -1):
            if row == 0 and trade[4] < data["Order Price"].iloc[row]:
                return -1
            if trade[4] >= data["Order Price"].iloc[row]:
                return row + 1

    elif trade[1] == "Buy":
        for row in range(len(data)):
            if row == len(data) - 1 and trade[4] >= data["Order Price"].iloc[row]:
                return len(data)
            if trade[4] < data["Order Price"].iloc[row]:
                return row - 1

# takes in the limit order book and finds the approximate appropriate prices for the market buy and market sell orders
# this will be defined as one tick above the highest limit price and one tick below the lowest limit price respectively
def find_market_order_prices(data: pd.DataFrame, tick=TICK) -> tuple:
    list_prices = list(np.array(data["Order Price"]))
    index_b = -1
    index_s = -1
    if 1000000.0 not in list_prices:
        market_buy = list_prices[-1] + tick
    # WARNING: this will break if there are only market orders in the order book
    else:
        index_b = list_prices.index(1000000.0)
        market_buy = list_prices[index_b - 1] + tick
    if 0.0 not in list_prices:
        market_sell = list_prices[0] - tick
    # WARNING: this will break if there are only market orders in the order book
    else:
        list_prices.reverse()
        index_s = len(list_prices) - 1 - list_prices.index(0.0)
        list_prices.reverse()
        market_sell = list_prices[index_s + 1] - tick
    return (market_buy, market_sell)

# extract only the selling side of the auction
def get_supply_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[["Selling Size", "Selling Trader", "Order Price"]].dropna().reset_index(drop=True)

# extract only the buying side of the auction
def get_demand_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[["Buying Size", "Buying Trader", "Order Price"]].dropna().reset_index(drop=True)

