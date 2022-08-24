import pandas as pd
import numpy as np

'''
    This file is to keep all the 'private' functions used in the uniform_pricing.py file.
'''

TICK = 0.1

# swap rows at index row1 and row2
def swap_rows(data: pd.DataFrame, row1: int, row2: int) -> pd.DataFrame:
    data1 = data.iloc[:min(row1, row2)]
    insert1 = data.iloc[[min(row1, row2)]]
    data2 = data.iloc[min(row1, row2) + 1: max(row1, row2)]
    insert2 = data.iloc[[max(row1, row2)]]
    data3 = data.iloc[max(row1, row2) + 1:]
    return pd.concat([data1, insert2, data2, insert1, data3]).reset_index(drop=True)

# swap rows if the prices are not in the correct order
# check both buy side going backward and sell side going forward
def check_invalid_price_order(data: pd.DataFrame) -> pd.DataFrame:
    copy_data = data
    for i in range(len(data) - 1, 0, -1):
        if data.at[i, "Buying Size"] is not None and data.at[i - 1, "Buying Size"] is not None and data.at[i - 1, "Order Price"] > data.at[i, "Order Price"]:
            copy_data = swap_rows(copy_data, i - 1, i)
    for i in range(len(data) - 1):
        if data.at[i, "Selling Size"] is not None and data.at[i + 1, "Selling Size"] is not None and data.at[i + 1, "Order Price"] < data.at[i, "Order Price"]:
            copy_data = swap_rows(copy_data, i, i + 1)
    return copy_data

# delete rows that have zeros as a check
def check_for_zeros(data: pd.DataFrame) -> pd.DataFrame:
    del_list = []
    for i in range(len(data)):
        if data["Selling Size"].iloc[i] == 0 or data["Buying Size"].iloc[i] == 0:
            del_list.append(i)
    data = data.drop(data.index[del_list])
    return data.reset_index(drop=True)

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

# check to see if a sell order added caused a trade
# and return the updated orderbook and trade summary
def check_sell_order_trades(data: pd.DataFrame, trade: list) -> tuple:
    index = list(data["Selling Trader"]).index(trade[0])

    trade_dict = {
        "Initiating Trader": [],
        "Passive Trader": [],
        "Amount": [],
        "Price Willing": [],
        "Price Paid": []
    }

    delete_indexes = []
    i = len(data) - 1
    market_buy, market_sell = find_market_order_prices(data)
    while data["Selling Size"].iloc[index] > 0 and i >= 0:
        if i == -1 or data["Order Price"].iloc[i] < data["Order Price"].iloc[index]:
            break
        if data["Buying Size"].iloc[i] is None or data["Buying Size"].iloc[i] == 0:
            i -= 1
            continue
        trading = min(data["Selling Size"].iloc[index], data["Buying Size"].iloc[i])
        data.at[index, "Selling Size"] -= trading
        data.at[i, "Buying Size"] -= trading
        trade_dict["Initiating Trader"].append(trade[0])
        trade_dict["Passive Trader"].append(data["Buying Trader"].iloc[i])
        trade_dict["Amount"].append(trading)
        trade_dict["Price Willing"].append(data["Order Price"].iloc[index])
        trade_dict["Price Paid"].append(data["Order Price"].iloc[i])
        if trade_dict["Price Willing"][-1] == 1000000.0:
            trade_dict["Price Willing"][-1] = market_buy
        if trade_dict["Price Paid"][-1] == 1000000.0:
            trade_dict["Price Paid"][-1] = market_buy
        if trade_dict["Price Willing"][-1] == 0.0:
            trade_dict["Price Willing"][-1] = market_sell
        if trade_dict["Price Paid"][-1] == 0.0:
            trade_dict["Price Paid"][-1] = market_sell
        if data["Selling Size"].iloc[index] == 0:
            delete_indexes.append(index)
            break
        if data["Buying Size"].iloc[i] == 0:
            delete_indexes.append(i)
            i -= 1

    data = data.drop(data.index[delete_indexes])
    return data.reset_index(drop=True), pd.DataFrame(trade_dict) if len(trade_dict["Initiating Trader"]) != 0 else None

# check to see if a buy order added caused a trade
# and return the updated orderbook and trade summary
def check_buy_order_trades(data: pd.DataFrame, trade: list) -> tuple:
    index = list(data["Buying Trader"]).index(trade[0])

    trade_dict = {
        "Initiating Trader": [],
        "Passive Trader": [],
        "Amount": [],
        "Price Willing": [],
        "Price Paid": []
    }

    delete_indexes = []
    i = 0
    market_buy, market_sell = find_market_order_prices(data)
    while data["Buying Size"].iloc[index] > 0 and i >= 0:
        if i == len(data) or data["Order Price"].iloc[i] > data["Order Price"].iloc[index]:
            break
        if data["Selling Size"].iloc[i] is None or data["Selling Size"].iloc[i] == 0:
            i += 1
            continue
        trading = min(data["Buying Size"].iloc[index], data["Selling Size"].iloc[i])
        data.at[index, "Buying Size"] -= trading
        data.at[i, "Selling Size"] -= trading
        trade_dict["Initiating Trader"].append(trade[0])
        trade_dict["Passive Trader"].append(data["Selling Trader"].iloc[i])
        trade_dict["Amount"].append(trading)
        trade_dict["Price Willing"].append(data["Order Price"].iloc[index])
        trade_dict["Price Paid"].append(data["Order Price"].iloc[i])
        if trade_dict["Price Willing"][-1] == 1000000.0:
            trade_dict["Price Willing"][-1] = market_buy
        if trade_dict["Price Paid"][-1] == 1000000.0:
            trade_dict["Price Paid"][-1] = market_buy
        if trade_dict["Price Willing"][-1] == 0.0:
            trade_dict["Price Willing"][-1] = market_sell
        if trade_dict["Price Paid"][-1] == 0.0:
            trade_dict["Price Paid"][-1] = market_sell
        if data["Buying Size"].iloc[index] == 0:
            delete_indexes.append(index)
            break
        if data["Selling Size"].iloc[i] == 0:
            delete_indexes.append(i)
            i += 1

    data = data.drop(data.index[delete_indexes])
    return data.reset_index(drop=True), pd.DataFrame(trade_dict) if len(trade_dict["Initiating Trader"]) != 0 else None


