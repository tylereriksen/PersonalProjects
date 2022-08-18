# NOT A FINISHED PRODUCT
# this code is to recreate a single price auction that uses uniform price distribution

import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# class for time to 
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


# this is a trade queue where people submit their auction bids and offers
TICK = 0.1
TRADE_QUEUE = [
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
    Trader("Sid").putOrder(2.0, "Sell", Time("10:29"), 19.8)
]
AUCTION_TIMES = [Time("10:00"), Time("10:30")]


# check to see if queue is in order of time
for idx, val in enumerate(TRADE_QUEUE[:-1]):
    if TRADE_QUEUE[idx + 1][3].compareTime(val[3]) == -1:
        print("ERROR")

# create the limit order book data for the above trade queue
OrderBook = pd.DataFrame().from_dict({
    "Selling Trader": [], 
    "Selling Size": [], 
    "Order Price": [], 
    "Buying Size": [],
    "Buying Trader": []
})


# -------------------------------------- THIS IS FOR ORDER BOOK --------------------------------------
# go through the trades in the queue and insert them into the data accordingly
# high bids and low asks get priority first
# if ask and bid prices are the sae, time priority is used
for trade in TRADE_QUEUE:
    index = 0
    outside_current_prices = True
    for i in range(len(OrderBook)):
        outside_current_prices = True
        if trade[1] == "Sell":
            if OrderBook.at[i, "Order Price"] > trade[4]:
                index = i
                outside_current_prices = False
                break
        else:
            if OrderBook.at[len(OrderBook) - i - 1, "Order Price"] < trade[4]:
                index = len(OrderBook) - i
                outside_current_prices = False
                break

    if outside_current_prices and len(OrderBook) != 0:
        if trade[1] == "Sell":
            if OrderBook.at[len(OrderBook) - 1, "Order Price"] < trade[4]:
                index = len(OrderBook)
            if OrderBook.at[len(OrderBook) - 1, "Order Price"] > trade[4]:
                index = 0
        elif trade[1] == "Buy":
            if OrderBook.at[0, "Order Price"] > trade[4]:
                index = 0
            if OrderBook.at[0, "Order Price"] > trade[4]:
                index = len(OrderBook)
    
    # the data to be inputted
    append_dict = {
        "Selling Trader": trade[0] if trade[1] == "Sell" else None,
        "Selling Size": trade[2] if trade[1] == "Sell" else None,
        "Order Price": trade[4],
        "Buying Size": trade[2] if trade[1] == "Buy" else None,
        "Buying Trader": trade[0] if trade[1] == "Buy" else None
    }
    new_entry = pd.DataFrame(append_dict, index = [index])
    if index == 0:
        OrderBook = pd.concat([new_entry, OrderBook]).reset_index(drop=True)
    elif index == len(OrderBook):
        OrderBook = pd.concat([OrderBook, new_entry]).reset_index(drop=True)
    elif trade[1] == "Sell":
        OrderBook = pd.concat([OrderBook[:index - 1], new_entry, OrderBook[index - 1:]]).reset_index(drop=True)
    else:
        OrderBook = pd.concat([OrderBook[:index + 1], new_entry, OrderBook[index + 1:]]).reset_index(drop=True)
    print("Updated Limit Order Book: ")
    print(OrderBook)
    print()


# -------------------------------- THIS IS FOR DEMAND AND SUPPLY GRAPH -------------------------------
# separate ask and bids into DEMAND and SUPPLY
# DEMAND is the bids since these people are demanding liquidity and instruments
# SUPPLY are the asks since these people are offering liquidity and instruments
DEMAND = OrderBook[["Buying Size", "Buying Trader", "Order Price"]].dropna().reset_index(drop=True)
SUPPLY = OrderBook[["Selling Size", "Selling Trader", "Order Price"]].dropna().reset_index(drop=True)

# demand when price is infinitely big is intuitively 0
D_Price = [np.inf]
D_Graph = [0]
for i in range(len(DEMAND)-1, -1, -1):
    D_Price.append(DEMAND["Order Price"].iloc[i])
    D_Price.append(DEMAND["Order Price"].iloc[i])
    D_Graph.append(D_Graph[-1])
    D_Graph.append(D_Graph[-1] + DEMAND["Buying Size"].iloc[i])
D_Price.append(0)
D_Graph.append(D_Graph[-1])

# supply wen price is 0 is intuitively 0
S_Price = [0]
S_Graph = [0]
for i in range(0, len(SUPPLY)):
    S_Price.append(SUPPLY["Order Price"].iloc[i])
    S_Price.append(SUPPLY["Order Price"].iloc[i])
    S_Graph.append(S_Graph[-1])
    S_Graph.append(S_Graph[-1] + SUPPLY["Selling Size"].iloc[i])
S_Price.append(1e6)
S_Graph.append(S_Graph[-1])

plt.plot(D_Price, D_Graph, 'r', label="Demand")
plt.plot(S_Price, S_Graph, 'b', label="Supply")
plt.plot(20, 11, 'kx', label="Equilibrium")
plt.legend()
plt.grid()
plt.title("SUPPLY AND DEMAND OF SINGLE PRICE AUCTION")
plt.xlim([19.7, 20.4])
plt.show()



# ---------------------------- FINDING THE AMOUNT TRADES AND PRICE TRADED ----------------------------
# We essentially try to find the point at which the supply and demand curves meet
# the x value is the price and the y value is amount traded
for idx, val in enumerate(S_Price):
    if S_Graph[idx] > D_Graph[len(D_Graph) - 1 - idx]:
        print()
        print("TRADES HAPPENED AT %f" %(val))
        trade_price = val
        print("THERE WERE A TOTAL OF %d INSTRUMENTS BEING TRADED" %(int(min(D_Graph[max(index for index, item in enumerate(D_Price) if item == val)], S_Graph[max(index for index, item in enumerate(S_Price) if item == val)]))))
        trade_vol = int(min(D_Graph[max(index for index, item in enumerate(D_Price) if item == val)], S_Graph[max(index for index, item in enumerate(S_Price) if item == val)]))
        break



# ---------------------------------- FINDING TRADER SURPLUS AMOUNTS ----------------------------------
trader_surpluses = {
    "Trader Name": [],
    "Trader Surplus": []
}   

def find_market_buy(data: pd.DataFrame, tick_size: float) -> float:
    data = data[data['Order Price'] != 1000000.0]
    return data["Order Price"].iloc[-1] + tick_size

def find_market_sell(data: pd.DataFrame, tick_size: float) -> float:
    data = data[data['Order Price'] != 0.0]
    return data["Order Price"].iloc[0] - tick_size

print(DEMAND)
print(SUPPLY)

buy_count = trade_vol
for idx in range(len(DEMAND) - 1, -1, -1):
    if buy_count == 0:
        trader_surpluses["Trader Name"].append(DEMAND["Buying Trader"].iloc[idx])
        trader_surpluses["Trader Surplus"].append(0.0)
        continue
    trader_surpluses["Trader Name"].append(DEMAND["Buying Trader"].iloc[idx])
    b_order_size = buy_count if buy_count < DEMAND["Buying Size"].iloc[idx] else DEMAND["Buying Size"].iloc[idx]
    buy_count -= b_order_size
    if DEMAND["Order Price"].iloc[idx] != 1000000.0:
        b_order_price = DEMAND["Order Price"].iloc[idx]
    else:
        b_order_price = find_market_buy(OrderBook, TICK)
        print(b_order_price)
    trader_surpluses["Trader Surplus"].append(round((b_order_price - trade_price) * b_order_size, 2))

sell_count = trade_vol
for idx in range(len(SUPPLY)):
    if sell_count == 0:
        trader_surpluses["Trader Name"].append(SUPPLY["Selling Trader"].iloc[idx])
        trader_surpluses["Trader Surplus"].append(0.0)
        continue
    trader_surpluses["Trader Name"].append(SUPPLY["Selling Trader"].iloc[idx])
    s_order_size = sell_count if sell_count < SUPPLY["Selling Size"].iloc[idx] else SUPPLY["Selling Size"].iloc[idx]
    sell_count -= s_order_size
    if SUPPLY["Order Price"].iloc[idx] != 0.0:
        s_order_price = SUPPLY["Order Price"].iloc[idx]
    else:
        s_order_price = find_market_sell(OrderBook, TICK)
    trader_surpluses["Trader Surplus"].append(round((trade_price - s_order_price) * s_order_size, 2))
print(pd.DataFrame.from_dict(trader_surpluses))


