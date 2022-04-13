import pandas as pd
import numpy as np

BUFFER = 0.5
TIMEDURATION = 1
INTERVAL = 0.25
ERROR_MESSAGE = "ERROR"

def roundUpNearestInterval(num):
    listHalf = list(np.arange(0,24, INTERVAL))
    intReturn = [x for x in listHalf if 0 <= x - num < INTERVAL]
    return intReturn[0]

def roundDownNearestInterval(num):
    listHalf = list(np.arange(0,24, INTERVAL))
    intReturn = [x for x in listHalf if 0 <= num - x < INTERVAL]
    return  intReturn[0]

def timeToNumber(stringTime):

    hrminList = stringTime.split(":")
    if not len(hrminList) == 2:
        return (ERROR_MESSAGE)

    try:
        hours = float(hrminList[0])
        min = float(hrminList[1])/60
    
    except:
        return (ERROR_MESSAGE)

    return (hours + min)

def numberToTime(numTime):

    # check if input is valid
    if type(numTime) == type("") or numTime < 0 or numTime >= 24:
        return ERROR_MESSAGE

    hours = int(numTime)
    min = str(int((numTime - hours) * 60))

    # case for when minutes is 0, or else it would be printed as ":0" instead of ":00"
    if min == "0":
        min = "00"

    return str(hours) + ":" + min


employeeWorkTimes = {
    'Employee Name': ['John Joe', 'Henry McGuire', 'Tony Toni'],
    'Shift Start Time': ['7:00', '10:30', '13:30'],
    'Shift End Time': ['14:00', '18:30', '21:00']
}
df = pd.DataFrame(data=employeeWorkTimes)

employeeWorkTimesDict = {}
for idx, num in enumerate(df['Employee Name']):
    employeeWorkTimesDict[num] = [df['Shift Start Time'][idx], df['Shift End Time'][idx]]

def employeesAvailableTimes(companyDict, timeDuration = TIMEDURATION):
    returnFixedDict = {}
    for idx, name in enumerate(companyDict.keys()):
        workingDef = companyDict[name]
        startTime = roundUpNearestInterval(timeToNumber(workingDef[0]))
        endTime = roundDownNearestInterval(timeToNumber(workingDef[1]))
        listOfTimes = list(numberToTime(x) for x in np.arange(startTime, endTime - TIMEDURATION + INTERVAL, INTERVAL))
        returnFixedDict[name] = listOfTimes

    return returnFixedDict

def numEmployeesPerTimes(companyDict):
    returnFixedDict = {}
    for x in np.arange(0, 24, INTERVAL):
        returnFixedDict[numberToTime(x)] = 0

    for employee in companyDict:
        for time in employeesAvailableTimes(companyDict)[employee]:
            returnFixedDict[time] += 1

    return returnFixedDict

def getCustomerAvailableTimes(companyDict):
    listCustomerTimes = []

    for time in numEmployeesPerTimes(companyDict):
        if numEmployeesPerTimes(companyDict)[time] != 0:
            listCustomerTimes.append(time)

    return listCustomerTimes

    

print(employeesAvailableTimes(employeeWorkTimesDict))
print(numEmployeesPerTimes(employeeWorkTimesDict))
print(getCustomerAvailableTimes(employeeWorkTimesDict))
