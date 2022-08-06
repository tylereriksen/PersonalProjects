import re

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
        if self.limit == "market":
            if self.bors == "buy":
                self.limit = 1000000
            elif self.bors == "sell":
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


trader1 = Trader("Bea")
trader1_info = trader1.putOrder(3, "buy", Time("10:01"), 20.0)
print(trader1_info)