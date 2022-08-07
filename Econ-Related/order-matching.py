import re
import pandas as pd

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
        hour2 = int(self.time[:self.time.index(":")])
        min2 = int(self.time[self.time.index(":") + 1:])
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

OrderBook = pd.DataFrame().from_dict({
    "Selling Trader": [], 
    "Selling Size": [], 
    "Order Price": [], 
    "Buyer Size": [],
    "Buyer Trader": []
    })

for i in range(TRADES["Name"]):
    trader = Trader(TRADES["Name"][i])
    trader.putOrder(TRADES["Order Number"][i], TRADES["Acquisition"][i], TRADES["Time"][i], TRADES["Limit"][i])
    


