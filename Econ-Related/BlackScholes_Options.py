import math
import numpy as np
from scipy import stats, optimize

def d1(underlying, strike, time, rate, sigma):
    d1 = (1 / (sigma * math.sqrt(time))) * (math.log(underlying / strike) + (rate + (sigma ** 2 / 2)) * time)
    return d1

def d2(underlying, strike, time, rate, sigma):
    d2 = d1(underlying, strike, time, rate, sigma) - sigma * math.sqrt(time)
    return d2

def option_val(underlying, strike, time, rate, sigma, optionType):
    cdf1 = stats.norm.cdf(optionType * d1(underlying, strike, time, rate, sigma))
    cdf2 = stats.norm.cdf(optionType * d2(underlying, strike, time, rate, sigma))
    option_val = optionType * cdf1 * underlying - optionType * cdf2 * strike * np.exp(-rate * time)
    return option_val

def findVol(underlying, strike, time, rate, price, optionType):
    myfunc = lambda x: option_val(underlying, strike, time, rate, x, optionType) - price
    minimum = 1e-9
    maximum = 10000
    try: 
        sigma = optimize.bisect(myfunc, minimum, maximum)
    except:
        sigma = minimum
    return sigma
