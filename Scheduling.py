import pandas as pd

employeeWorkTimes = {
    'Employee Name': ['John Joe', 'Henry McGuire', 'Tony Toni'],
    'Shift Start Time': ['7:30', '10:30', '13:30'],
    'Shift End Time': ['2:00', '18:30', '21:00']
}
df = pd.DataFrame(data=employeeWorkTimes)

employeeWorkTimesDict = {}
for idx, num in enumerate(df['Employee Name']):
    employeeWorkTimesDict[num] = [df['Shift Start Time'][idx], df['Shift End Time'][idx]]
print(employeeWorkTimesDict)