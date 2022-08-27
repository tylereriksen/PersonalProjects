'''
    Python functions to calculate Black Scholes and the Greeks for options.
'''

import math
import numpy as np
from scipy import stats, optimize

def d1(underlying, strike, time, rate, volatility):
    d1 = (1 / (volatility * math.sqrt(time))) * (math.log(underlying / strike) + (rate + (volatility ** 2 / 2)) * time)
    return d1

def d2(underlying, strike, time, rate, volatility):
    d2 = d1(underlying, strike, time, rate, volatility) - volatility * math.sqrt(time)
    return d2

def option_val(underlying, strike, time, rate, volatility, optionType):
    cdf1 = stats.norm.cdf(optionType * d1(underlying, strike, time, rate, volatility))
    cdf2 = stats.norm.cdf(optionType * d2(underlying, strike, time, rate, volatility))
    option_val = optionType * cdf1 * underlying - optionType * cdf2 * strike * np.exp(-rate * time)
    return option_val

def findVol(underlying, strike, time, rate, price, optionType):
    myfunc = lambda x: option_val(underlying, strike, time, rate, x, optionType) - price
    minimum = 1e-9
    maximum = 10000
    try: 
        volatility = optimize.bisect(myfunc, minimum, maximum)
    except:
        volatility = minimum
    return volatility

def Delta(underlying, strike, time, rate, volatility, optionType):
    return optionType * stats.norm.cdf(optionType * d1(underlying, strike, time, rate, volatility))

def Gamma(underlying, strike, time, rate, volatility, optionType):
    return stats.norm.pdf(d1(underlying, strike, time, rate, volatility)) / (strike * volatility * math.sqrt(time))

def Vega(underlying, strike, time, rate, volatility, optionType):
    return underlying * stats.norm.pdf(d1(underlying, strike, time, rate, volatility)) * math.sqrt(time)

def Theta(underlying, strike, time, rate, volatility, optionType):
    d1 = d1(underlying, strike, time, rate, volatility)
    d2 = d2(underlying, strike, time, rate, volatility)
    return -underlying * stats.norm.pdf(d1) * volatility / (2 * math.sqrt(time)) + optionType * rate * strike * np.exp(-rate * time) * stats.norm.cdf(optionType * d2)

