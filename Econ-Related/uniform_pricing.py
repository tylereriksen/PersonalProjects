import re
import pandas as pd
import matplotlib.pyplot as plt
from trading_and_pricing_functions import *

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

TICK = 0.1 # minimum price increment needed to make a new different price bid or ask
AUCTION_INTERVALS = [Time("10:00"), Time("10:30")]
QUEUE = [
    Trader("Sad").putOrder(4.0, "Sell", Time("09:59"), 'Market'), # this is to test if the functions work when dealing with trades outside auction times
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
    Trader("Sid").putOrder(2.0, "Sell", Time("10:29"), 19.8),
    Trader("Bad").putOrder(1.0, "Buy", Time("10:31"), 20.1),
]


# get a trade and append this trade into the limit order book at the right place
def update_orderbook(trade: list, data=None):
    if data is None:
        return generate_new_orderbook_row(trade)
    index = find_index_to_update(data, trade)
    append_row = generate_new_orderbook_row(trade)
    if index == -1:
        return pd.concat([append_row, data]).reset_index(drop=True)
    if index == len(data):
        return pd.concat([data, append_row]).reset_index(drop=True)
    return pd.concat([data.iloc[ :index], append_row, data.iloc[index: ]]).reset_index(drop=True)

# replaces the fillin values for market orders with their approximate appropriate values
def replace_market_placeholders(data: pd.DataFrame, tick=TICK) -> pd.DataFrame:
    market_b, market_s = find_market_order_prices(data, tick)
    for i in range(len(data)):
        if data.at[i, "Order Price"] == 0.0:
            data.at[i, "Order Price"] = market_s
        elif data.at[i, "Order Price"] ==  1000000.0:
            data.at[i, "Order Price"] = market_b
    return data

# get the supply data and put it in the form of a price vs quantity supplied plot
def get_supply_graph(data: pd.DataFrame) -> tuple:
    sup_data = get_supply_data(data)
    price = [0]
    supply = [0]
    for i in range(len(sup_data)):
        price.append(sup_data["Order Price"].iloc[i])
        price.append(sup_data["Order Price"].iloc[i])
        supply.append(supply[-1])
        supply.append(supply[-1] + sup_data["Selling Size"].iloc[i])
    price.append(1e6) # place holder
    supply.append(supply[-1])
    return (price, supply)

# get the demand data and put it in the form of a price vs quantity demanded plot
def get_demand_graph(data: pd.DataFrame) -> tuple:
    dem_data = get_demand_data(data)
    price = [1e6]
    demand = [0]
    for i in range(len(dem_data) - 1, -1, -1):
        price.append(dem_data["Order Price"].iloc[i])
        price.append(dem_data["Order Price"].iloc[i])
        demand.append(demand[-1])
        demand.append(demand[-1] + dem_data["Buying Size"].iloc[i])
    price.append(0)
    demand.append(demand[-1])
    return (price, demand)

def get_equilibrium(data: pd.DataFrame) -> tuple:
    sup_data = get_supply_data(data)
    dem_data = get_demand_data(data)
    quantity = 0
    last_trade = (-1, -1)
    sup_ct = 0
    dem_ct = len(dem_data) - 1
    while sup_ct < len(sup_data) and dem_ct > -1 and sup_data["Order Price"].iloc[sup_ct] <= dem_data["Order Price"].iloc[dem_ct]:
        amount = min(sup_data["Selling Size"].iloc[sup_ct], dem_data["Buying Size"].iloc[dem_ct])
        sup_data.at[sup_ct, "Selling Size"] -= amount
        dem_data.at[dem_ct, "Buying Size"] -= amount
        quantity += amount
        last_trade = (sup_data["Order Price"].iloc[sup_ct], dem_data["Order Price"].iloc[dem_ct])
        print(sup_data["Selling Trader"].iloc[sup_ct], "and", dem_data["Buying Trader"].iloc[dem_ct], "traded", str(amount), "amount.")
        if sup_data["Selling Size"].iloc[sup_ct] == 0:
            if dem_data["Buying Size"].iloc[dem_ct] == 0:
                sup_ct += 1
                dem_ct -= 1
            else:
                sup_ct += 1
        elif dem_data["Buying Size"].iloc[dem_ct] == 0:
            dem_ct -= 1

    if last_trade[0] == last_trade[1]:
        return quantity, last_trade[0], None
    else:
        return quantity, last_trade[0], last_trade[1]
        

#----------------------------------------------------------------------------------------------------------------------

def main():
    ORDERBOOK = None
    for trade in QUEUE:
        if trade[3].compareTime(AUCTION_INTERVALS[1]) == -1 and trade[3].compareTime(AUCTION_INTERVALS[0]) != -1:
            ORDERBOOK = update_orderbook(trade, ORDERBOOK)
            print("UPDATED ORDER BOOK:")
            print(ORDERBOOK)
            print()
        elif trade[3].compareTime(AUCTION_INTERVALS[1]) != -1:
            break
    ORDERBOOK = replace_market_placeholders(ORDERBOOK)
    print("FINAL ORDER BOOK OF THE AUCTION SESSION:")
    print(ORDERBOOK)
    return ORDERBOOK

def graph(data: pd.DataFrame, equ_qty=None, equ_px=None):
    sup_px, sup = get_supply_graph(data)
    dem_px, dem = get_demand_graph(data)
    plt.plot(sup_px, sup, 'r', label="supply")
    plt.plot(dem_px, dem, 'b', label="demand")
    if equ_qty is not None and equ_px is not None and not isinstance(equ_px, list):
        plt.plot([equ_px], [equ_qty], 'kx', label="equilibrium")
    plt.xlabel("Prices")
    plt.ylabel("Quantity")
    plt.xlim([min(sup_px[1], dem_px[1]) - 2 * TICK, max(sup_px[-2], dem_px[-2]) + 2 * TICK])
    plt.title("Supply and Demand")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    ORDERBOOK = main()
    qty, px, _ = get_equilibrium(ORDERBOOK)
    if _ is not None:
        px = [px, _]
    graph(ORDERBOOK, qty, px)