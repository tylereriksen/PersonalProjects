# NOT A FINISHED PRODUCT
# this code is to recreate a single price auction that uses uniform price distribution

import re
import pandas as pd

# class for a Trader
# will contain trader name, trade size, trade type, trade limit, and time executed
class Trader():
    def __init__(self, name):
        self.name = name
        self.bors = ""
        self.amount = 0
        self.time = ""
        self.limit = 0

    def putOrder(self, amount, bors, time, limit):
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

# class for time to 
class Time():
    def __init__(self, time):
        regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
        p = re.compile(regex)
        if time == "":
            raise Exception("Invalid Time String")
        m = re.search(p, time)
        if m is None :
            raise Exception("Invalid Time String")
        self.time = time

    def compareTime(self, other):
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


TRADES = {
    "Name": ["Bea", "Sam", "Ben", "Sol", "Stu", "Bif", "Bob", "Sue", "Bud"],
    "Order Number": [3, 2, 2, 1, 5, 4, 2, 6, 7],
    "Acquisition": ["Buy", "Sell", "Buy", "Sell", "Sell", "Buy", "Buy", "Sell", "Buy"],
    "Time": [Time("10:01"), Time("10:05"), Time("10:08"), Time("10:09"), Time("10:10"), Time("10:15"), Time("10:18"), Time("10:20"), Time("10:29")],
    "Limit": [20.0, 20.1, 20.0, 19.8, 20.2, "Market", 20.1, 20.0, 19.8]
}

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
    Trader("Bud").putOrder(7.0, "Buy", Time("10:29"), 19.8)
]
AUCTION_TIMES = [Time("10:00"), Time("10:30")]


# check to see if queue is in order of time
for idx, val in enumerate(TRADE_QUEUE[:-1]):
    if TRADE_QUEUE[idx + 1][3].compareTime(val[3]) == -1:
        print("ERROR")

OrderBook = pd.DataFrame().from_dict({
    "Selling Trader": [], 
    "Selling Size": [], 
    "Order Price": [], 
    "Buying Size": [],
    "Buying Trader": []
})

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
    

    append_dict = {
        "Selling Trader": trade[0] if trade[1] == "Sell" else "",
        "Selling Size": trade[2] if trade[1] == "Sell" else "",
        "Order Price": trade[4],
        "Buying Size": trade[2] if trade[1] == "Buy" else "",
        "Buying Trader": trade[0] if trade[1] == "Buy" else ""
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

