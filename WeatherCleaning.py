import pandas as pd
import numpy as np

dfNew = pd.read_csv('weatherAfterMerge.csv' , sep=',', encoding='latin1')
## Fix snow missing data. If minimum temp > 32 then it's impossible to have snow
snowNAList = dfNew[dfNew['SNOW'].isnull()].index.tolist()
for i in snowNAList:
    date = dfNew.iloc[i]['Date']
    if(any(dfNew[dfNew['Date']==date]['TMIN'] > 32)):
        dfNew.loc[i,'SNOW'] = 0
    
## see how it improves after replacing the missing values
# print(dfNew['SNOW'].isnull().values.ravel().sum())
# 243
# This step reduces missing data from 1500 to 243
        
## Replace rest of the missing values by taking mean of the snow data for that day
## Update missing value list
snowNAList = dfNew[dfNew['SNOW'].isnull()].index.tolist()
for i in snowNAList:
    date = dfNew.iloc[i]['Date']
    if(not all(val is None for val in dfNew[dfNew['Date']==date]['SNOW'])):
        mean = np.mean(dfNew[dfNew['Date']==date]['SNOW'])
        dfNew.loc[i,'SNOW'] = mean
# print(dfNew['SNOW'].isnull().values.ravel().sum())
# 10
# The missing value reduced from about 1500 entries to 10 entries 

## correct incorrect data in SNOW
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['SNOW']) - min(dfNew[dfNew['Date']==date]['SNOW']))>2):
        mean = np.mean(dfNew[dfNew['Date']==date]['SNOW'])
        dfNew.loc[dfNew['Date']==date,'SNOW'] = mean
        
## Rerun cleanliness and see how it improves 
count = 0
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['SNOW']) - min(dfNew[dfNew['Date']==date]['SNOW']))>2):
        count = count+1
# print(count)
# 0 
# Number of incorrect values reduces to zero

## Fix missing values in PRCP 
## Replace missing values using mean of PRCP for that day
PRCPNAList = dfNew[dfNew['PRCP'].isnull()].index.tolist()
for i in PRCPNAList:
    date = dfNew.iloc[i]['Date']
    if(not all(val is None for val in dfNew[dfNew['Date']==date]['PRCP'])):
        mean = np.mean(dfNew[dfNew['Date']==date]['PRCP'])
        dfNew.loc[i,'PRCP'] = mean
# print(dfNew['PRCP'].isnull().values.ravel().sum())
# 4
# Nuber of missing values reduces from 21 to 4 
# print(dfNew[dfNew['PRCP'].isnull()])
#                     Date     Location  PRCP  SNOW  TMAX  TMIN
#1091  2016-01-23T00:00:00  USC00186350   NaN  14.0  29.0  22.0
#1092  2016-01-24T00:00:00  USC00186350   NaN  12.0  35.0  18.0
#2525  2016-01-23T00:00:00  USC00182325   NaN  14.0  28.0  20.0
#2526  2016-01-24T00:00:00  USC00182325   NaN  12.0  26.0  19.0

# The days of the four missing values had heavy snow. We can replace the missing values
# into 0 for those two days 
for i in dfNew[dfNew['PRCP'].isnull()].index.tolist():
    dfNew.loc[i,'PRCP'] = 0
    
# print(dfNew['PRCP'].isnull().values.ravel().sum())
# 0 
    
# Correct incorrect data in PRCP by taking mean PRCP for that day
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['PRCP']) - min(dfNew[dfNew['Date']==date]['PRCP']))>1):
        mean = np.mean(dfNew[dfNew['Date']==date]['PRCP'])
        dfNew.loc[dfNew['Date']==date,'PRCP'] = mean
        
count = 0
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['PRCP']) - min(dfNew[dfNew['Date']==date]['PRCP']))>1):
        count = count+1
# print(count)
# 0
# After fixing PRCP, the number of missing values and incorrect values reduces to zero

dfNew.to_csv('weatherAfterCleaning.txt',sep = '|', index = False)
dfNew.to_csv('weatherAfterCleaning.csv',sep = ',', index = False)
