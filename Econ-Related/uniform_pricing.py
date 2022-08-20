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
    Trader("Sad").putOrder(4.0, "Sell", Time("09:59"), 'Market'),
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

# replaces the fillin values for market orders with their approximate appropriate values
def replace_market_placeholders(data: pd.DataFrame, tick=TICK) -> pd.DataFrame:
    market_b, market_s = find_market_order_prices(data, tick)
    for i in range(len(data)):
        if data.at[i, "Order Price"] == 0.0:
            data.at[i, "Order Price"] = market_s
        elif data.at[i, "Order Price"] ==  1000000.0:
            data.at[i, "Order Price"] = market_b
    return data

def get_supply_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[["Selling Size", "Selling Trader", "Order Price"]].dropna().reset_index(drop=True)

def get_demand_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[["Buying Size", "Buying Trader", "Order Price"]].dropna().reset_index(drop=True)

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

def graph(data: pd.DataFrame):
    sup_px, sup = get_supply_graph(data)
    dem_px, dem = get_demand_graph(data)
    plt.plot(sup_px, sup, 'r', label="supply")
    plt.plot(dem_px, dem, 'b', label="demand")
    plt.xlabel("Prices")
    plt.ylabel("Quantity")
    plt.xlim([min(sup_px[1] - 2 * TICK, dem_px[1] - 2 * TICK), max(sup_px[-2] + 2 * TICK, dem_px[-2] + 2 * TICK)])
    plt.title("Supply and Demand")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    ORDERBOOK = main()
    graph(ORDERBOOK)