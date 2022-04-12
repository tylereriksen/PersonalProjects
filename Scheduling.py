import pandas as pd
import numpy as np

def roundUpNearestHalf(num):
    listHalf = list(np.arange(0,24, 0.5))
    intReturn = [x for x in listHalf if 0 <= x - num < 0.5]
    return intReturn[0]

def roundDownNearestHalf(num):
    listHalf = list(np.arange(0,24, 0.5))
    intReturn = [x for x in listHalf if 0 <= num - x < 0.5]
    return  intReturn[0]




employeeWorkTimes = {
    'Employee Name': ['John Joe', 'Henry McGuire', 'Tony Toni'],
    'Shift Start Time': ['7:30', '10:30', '13:30'],
    'Shift End Time': ['2:00', '18:30', '21:00']
}
df = pd.DataFrame(data=employeeWorkTimes)

employeeWorkTimesDict = {}
for idx, num in enumerate(df['Employee Name']):
    employeeWorkTimesDict[num] = [df['Shift Start Time'][idx], df['Shift End Time'][idx]]