# NOT FINISHED
import re
import pandas as pd
from trading_and_pricing_functions import *


# class for time
class Time():
    def __init__(self, time: str):
        regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
        p = re.compile(regex)
        if time == "":
            raise Exception("Invalid Time String")
        m = re.search(p, time)
        if m is None :
            raise Exception("Invalid Time String")
        self.time = time

    def compareTime(self, other) -> int:
        hour1 = int(self.time[:self.time.index(":")])
        min1 = int(self.time[self.time.index(":") + 1:])
        hour2 = int(other.time[:self.time.index(":")])
        min2 = int(other.time[self.time.index(":") + 1:])
        if hour1 > hour2:
            return 1
        if hour1 < hour2:
            return -1
        if min1 > min2:
            return 1
        if min1 < min2:
            return -1
        return 0

    def convert_time_to_float(self) -> float:
        hour = int(self.time[:self.time.index(":")])
        min = int(self.time[self.time.index(":") + 1: ])
        return hour + (min / 60)

# class for a Trader
# will contain trader name, trade size, trade type, trade limit, and time executed
class Trader():
    def __init__(self, name: str):
        self.name = name
        self.bors = ""
        self.amount = 0
        self.time = ""
        self.limit = 0

    def putOrder(self, amount: float, bors: str, time: Time, limit: float) -> list:
        self.bors = bors
        self.amount = amount
        self.time = time
        self.limit = limit
        if self.limit == "Market":
            if self.bors == "Buy":
                self.limit = 1000000
            elif self.bors == "Sell":
                self.limit = 0
        return [self.name, self.bors, self.amount, self.time, self.limit]


TICK = 0.1
QUEUE = [
    Trader("Bea").putOrder(3.0, "Buy", Time("10:01"), 20.0),
    Trader("Sam").putOrder(2.0, "Sell", Time("10:05"), 20.1),
    Trader("Ben").putOrder(2.0, "Buy", Time("10:08"), 20.0),
    Trader("Sol").putOrder(1.0, "Sell", Time("10:09"), 19.8),
    Trader("Stu").putOrder(5.0, "Sell", Time("10:10"), 20.2),
    Trader("Bif").putOrder(4.0, "Buy", Time("10:15"), 'Market'),
    Trader("Bob").putOrder(2.0, "Buy", Time("10:18"), 20.1),
    Trader("Sue").putOrder(6.0, "Sell", Time("10:20"), 20.0),
    Trader("Sos").putOrder(3.0, "Sell", Time("10:25"), 20.0),
    Trader("Bud").putOrder(7.0, "Buy", Time("10:27"), 19.8),
    Trader("Sid").putOrder(2.0, "Sell", Time("10:29"), 19.8)]


# get a trade and append this trade into the limit order book at the right place
def update_orderbook(trade: list, data=None) -> pd.DataFrame:
    if data is None:
        return generate_new_orderbook_row(trade)
    index = find_index_to_update(data, trade)
    append_row = generate_new_orderbook_row(trade)
    if index == -1:
        return pd.concat([append_row, data]).reset_index(drop=True)
    if index == len(data):
        return pd.concat([data, append_row]).reset_index(drop=True)
    return pd.concat([data.iloc[ :index], append_row, data.iloc[index: ]]).reset_index(drop=True)

def check_sell_order_trades(data: pd.DataFrame, trade: list):
    index = list(data["Selling Trader"]).index(trade[0])

    delete_indexes = []
    i = len(data) - 1
    while data["Selling Size"].iloc[index] > 0 and i >= 0:
        if data["Order Price"].iloc[i] < data["Order Price"].iloc[index]:
            break
        if data["Buying Size"].iloc[i] is None or data["Buying Size"].iloc[i] == 0:
            i -= 1
            continue
        trading = min(data["Selling Size"].iloc[index], data["Buying Size"].iloc[i])
        data.at[index, "Selling Size"] -= trading
        data.at[i, "Buying Size"] -= trading
        if data["Selling Size"].iloc[index] == 0:
            delete_indexes.append(index)
            break
        if data["Buying Size"].iloc[i] == 0:
            delete_indexes.append(i)
            i -= 1

    data = data.drop(data.index[delete_indexes])
    return data.reset_index(drop=True)

        


ORDERBOOK = None
for trade in QUEUE:
    ORDERBOOK = update_orderbook(trade, ORDERBOOK)
    print(ORDERBOOK)

ORDERBOOK = update_orderbook(Trader("Sad").putOrder(10.0, "Sell", Time("10:30"), 20.0), ORDERBOOK)
a = check_sell_order_trades(ORDERBOOK, Trader("Sad").putOrder(10.0, "Sell", Time("10:30"), 20.2))
print(a)

