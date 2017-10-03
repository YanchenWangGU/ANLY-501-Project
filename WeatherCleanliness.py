import pandas as pd

dfNew = pd.read_csv('weatherAfterMerge.csv' , sep=',', encoding='latin1')
## test number of missing values for attributes PRCP, SNOW, 
## Tmax, Tmin(Tmax, Tmin are only for the first two locations)
missVal= {}
missVal['Date'] = dfNew['Date'].isnull().values.ravel().sum()
missVal['PRCP'] = dfNew['PRCP'].isnull().values.ravel().sum()
missVal['SNOW'] = dfNew['SNOW'].isnull().values.ravel().sum()
missVal['TMIN'] = dfNew[dfNew['Location'] != 'US1VAFX0063']['TMIN'].isnull().values.ravel().sum()
missVal['TMAX'] = dfNew[dfNew['Location'] != 'US1VAFX0063']['TMIN'].isnull().values.ravel().sum()
## missVal:{'Date': 0, 'PRCP': 35, 'SNOW': 1495, 'TMAX': 24, 'TMIN': 24}

fracNa = {}
for i in missVal:
    fracNa[i] = missVal[i]/len(dfNew.index)

# print(fracNa)
# fracNa:{'Date': 0.0, 'PRCP': 0.0087194818136522179, 'SNOW': 0.37244643746885897, 
# 'TMIN': 0.0059790732436472349, 'TMAX': 0.0059790732436472349}
# SNOW has the most missing values 

noiseVal = {}
## Check for noise values in Date. There are 365*3+366 = 1461 days in the four years 
## and we can see if the number of unique values == 1461
noiseVal['Date'] = len(pd.unique(dfNew['Date'])) - 1461
count = 0
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['PRCP']) - min(dfNew[dfNew['Date']==date]['PRCP']))>1):
        count = count+1
noiseVal['PRCP'] = count

count = 0
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['SNOW']) - min(dfNew[dfNew['Date']==date]['SNOW']))>2):
        count = count+1
noiseVal['SNOW'] = count

count = 0
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['TMAX']) - min(dfNew[dfNew['Date']==date]['TMAX']))>10):
        count = count+1
noiseVal['TMAX'] = count

count = 0
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['TMIN']) - min(dfNew[dfNew['Date']==date]['TMIN']))>10):
        count = count+1
noiseVal['TMIN'] = count
# noiseVal:{'Date': 0, 'PRCP': 21, 'SNOW': 6, 'TMAX': 47, 'TMIN': 29}

fracNoise = {}
for i in noiseVal:
    fracNoise[i] = noiseVal[i]/len(dfNew.index)
    
# print(fracNoise)
# fracNoise:{'Date': 0.0, 'PRCP': 0.00523168908819133, 'SNOW': 0.0014947683109118087,
# 'TMAX': 0.011709018435475834, 'TMIN': 0.007224713502740409}
# We can see that PRCP has the most noise values 