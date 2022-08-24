'''
    This file is to show how in a continuous auction, how the discriminatory
    pricing rule works. The functions in this file will show how the orderbook
    gets updated after every trade, how it finds if any trades happened with
    the placement of that order, how the tradebook summary gets updated, and
    the trader surpluses for each individual trader. One key observation is 
    that if traders placed their orders in the same order, amount, quantity,
    and limit prices for both a single-sided and continuous auction, then
    the uniform pricing rule will always generate most trader surplus comp-
    pared to the discriminatory pricing rule.
'''

# import packages
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

# check to see if an order caused a trade and return the updated orderbook along with trade summary
# trades happen at the limit price of the trader who had their order already put previously (must be
# 'better' or equal to the limit price of the last trader to place their orders)
def check_order_trades(data: pd.DataFrame, trade: list) -> tuple:
    if trade[1] == "Sell":
        data, tradebook = check_sell_order_trades(data, trade)
    elif trade[1] == "Buy":
        data, tradebook = check_buy_order_trades(data, trade)
    data = check_for_zeros(data)
    return data, tradebook

# get the tradebook summaries and find each individual trader's surpluses from their trades
def get_trader_surplus(tradebook: pd.DataFrame) -> pd.DataFrame:
    surplus_data = {
        "Trader": [],
        "Traded Amount": [],
        "Average Surplus": [],
        "Total Surplus": []
    }
    names = set(list(tradebook["Initiating Trader"]) + list(tradebook["Passive Trader"]))
    for name in names:
        surplus_data["Trader"].append(name)
        count_trd = 0
        surplus = 0
        indices1 = np.where(np.array(tradebook["Initiating Trader"]) == name)[0]
        for index in indices1:
            count_trd += tradebook["Amount"].iloc[index]
            surplus += abs(tradebook["Price Willing"].iloc[index] - tradebook["Price Paid"].iloc[index]) * tradebook["Amount"].iloc[index]
        indices2 = np.where(np.array(tradebook["Passive Trader"]) == name)[0]
        for index in indices2:
            count_trd += tradebook["Amount"].iloc[index]
        surplus_data["Traded Amount"].append(count_trd)
        surplus_data["Average Surplus"].append(surplus / count_trd)
        surplus_data["Total Surplus"].append(surplus)

    surplus_data = pd.DataFrame(surplus_data).sort_values(by = ["Total Surplus", "Average Surplus"], ascending=False).reset_index(drop=True)
    return surplus_data


#----------------------------------------------------------------------------------------------------------------------

# go through the queue and update the orderbook after each order
# alsoupdate the tradebook summaries after each order as well
def main() -> tuple:
    ORDERBOOK = None
    TRADES = None
    for trade in QUEUE:
        ORDERBOOK = check_invalid_price_order(update_orderbook(trade, ORDERBOOK))
        print("UPDATED ORDER BOOK:")
        print(ORDERBOOK)
        print()
        print("CHECKING TRADES...")
        ORDERBOOK, tradebook = check_order_trades(ORDERBOOK, trade)
        if tradebook is None:
            print("NO TRADES HAPPENED")
            print()
        else:
            print("TRADES THAT HAPPENED:")
            print(tradebook)
            TRADES = pd.concat([TRADES, tradebook]).reset_index(drop=True)
            print()
            print("UPDATED ORDERBOOK WITH TRADES:")
            print(ORDERBOOK)
            print()
    print()
    print("FINAL ORDERBOOK OF THE QUEUE:")
    print(ORDERBOOK)
    print()
    print("FINAL TRADEBOOK:")
    print(TRADES)
    print()
    return ORDERBOOK, TRADES

# get the tradebook summaries and return the trader surplus summary
def surplus(tradebook: pd.DataFrame) -> pd.DataFrame:
    tradesurplus = get_trader_surplus(tradebook)
    print("TRADER SURPLUSES:")
    print(tradesurplus)
    return tradesurplus

if __name__ == "__main__":
    ORDERBOOK, TRADES = main()
    SURPLUS = surplus(TRADES)

