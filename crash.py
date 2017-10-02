#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 21:27:40 2017

@author: FrankWang
"""

import requests
import pandas as pd

df = pd.DataFrame()
BaseURL="https://opendata.arcgis.com/datasets/70392a096a8e431381f1f692aaa06afd_24.geojson"
response=requests.get(BaseURL)
jsontxt = response.json()
for dict in jsontxt:
    print(dict[0])

def getCrashAPI():
    BaseURL = "https://opendata.arcgis.com/datasets/70392a096a8e431381f1f692aaa06afd_24.geojson"
    response=requests.get(BaseURL)
    df = pd.DataFrame()
    
    jsontxt = response.json()
    my_list = list()
    values = {'2013','2014','2015','2016'}
    
    for i in range(len(jsontxt['features'])):
        FromYr = jsontxt['features'][i]['properties']['FROMDATE']
        ReportYr = jsontxt['features'][i]['properties']['REPORTDATE']
        if (FromYr is not None and ReportYr is not None):
            if (FromYr.split("-")[0] in values and ReportYr.split("-")[0] in values):
                my_list.append(i)   
    
    for i in my_list:
        FROMDATE = jsontxt['features'][i]['properties']['FROMDATE']
        REPORTDATE = jsontxt['features'][i]['properties']['REPORTDATE']
        ADDRESS = jsontxt['features'][i]['properties']['ADDRESS']
        LATITUDE = jsontxt['features'][i]['properties']['LATITUDE']
        LONGITUDE = jsontxt['features'][i]['properties']['LONGITUDE']
        MAJORINJURIES_BICYCLIST = jsontxt['features'][i]['properties']['MAJORINJURIES_BICYCLIST']
        MINORINJURIES_BICYCLIST = jsontxt['features'][i]['properties']['MINORINJURIES_BICYCLIST']
        UNKNOWNINJURIES_BICYCLIST = jsontxt['features'][i]['properties']['UNKNOWNINJURIES_BICYCLIST']
        FATAL_BICYCLIST = jsontxt['features'][i]['properties']['FATAL_BICYCLIST']
        MAJORINJURIES_DRIVER = jsontxt['features'][i]['properties']['MAJORINJURIES_DRIVER']
        MINORINJURIES_DRIVER = jsontxt['features'][i]['properties']['MINORINJURIES_DRIVER']
        UNKNOWNINJURIES_DRIVER = jsontxt['features'][i]['properties']['UNKNOWNINJURIES_DRIVER']
        FATAL_DRIVER = jsontxt['features'][i]['properties']['FATAL_DRIVER']
        MAJORINJURIES_PEDESTRIAN = jsontxt['features'][i]['properties']['MAJORINJURIES_PEDESTRIAN']
        MINORINJURIES_PEDESTRIAN = jsontxt['features'][i]['properties']['MINORINJURIES_PEDESTRIAN']
        UNKNOWNINJURIES_PEDESTRIAN = jsontxt['features'][i]['properties']['UNKNOWNINJURIES_PEDESTRIAN']
        FATAL_PEDESTRIAN = jsontxt['features'][i]['properties']['FATAL_PEDESTRIAN']
        TOTAL_VEHICLES = jsontxt['features'][i]['properties']['TOTAL_VEHICLES']
        TOTAL_BICYCLES = jsontxt['features'][i]['properties']['TOTAL_BICYCLES']
        TOTAL_PEDESTRIANS = jsontxt['features'][i]['properties']['TOTAL_PEDESTRIANS']
        PEDESTRIANSIMPAIRED = jsontxt['features'][i]['properties']['PEDESTRIANSIMPAIRED']
        BICYCLISTSIMPAIRED = jsontxt['features'][i]['properties']['BICYCLISTSIMPAIRED']
        DRIVERSIMPAIRED = jsontxt['features'][i]['properties']['DRIVERSIMPAIRED']
        TOTAL_TAXIS = jsontxt['features'][i]['properties']['TOTAL_TAXIS']
        TOTAL_GOVERNMENT = jsontxt['features'][i]['properties']['TOTAL_GOVERNMENT']
        SPEEDING_INVOLVED = jsontxt['features'][i]['properties']['SPEEDING_INVOLVED']
    
        dat = pd.DataFrame({'FROMDATE': [FROMDATE],'REPORTDATE':[REPORTDATE],
                            'ADDRESS':[ADDRESS],'LATITUDE':[LATITUDE],'LONGITUDE':[LONGITUDE],
                            'MAJORINJURIES_BICYCLIST':[MAJORINJURIES_BICYCLIST],'MINORINJURIES_BICYCLIST':[MINORINJURIES_BICYCLIST],
                            'UNKNOWNINJURIES_BICYCLIST':[UNKNOWNINJURIES_BICYCLIST],'FATAL_BICYCLIST':[FATAL_BICYCLIST],
                            'MAJORINJURIES_DRIVER':[MAJORINJURIES_DRIVER],'MINORINJURIES_DRIVER':[MINORINJURIES_DRIVER],
                            'UNKNOWNINJURIES_DRIVER':[UNKNOWNINJURIES_DRIVER],'FATAL_DRIVER':[FATAL_DRIVER],
                            'MAJORINJURIES_PEDESTRIAN':[MAJORINJURIES_PEDESTRIAN],'MINORINJURIES_PEDESTRIAN':[MINORINJURIES_PEDESTRIAN],
                            'UNKNOWNINJURIES_PEDESTRIAN':[UNKNOWNINJURIES_PEDESTRIAN],'FATAL_PEDESTRIAN':[FATAL_PEDESTRIAN],
                            'TOTAL_VEHICLES':[TOTAL_VEHICLES],'TOTAL_BICYCLES':[TOTAL_BICYCLES],'TOTAL_PEDESTRIANS':[TOTAL_PEDESTRIANS],
                            'PEDESTRIANSIMPAIRED':[PEDESTRIANSIMPAIRED],'BICYCLISTSIMPAIRED':[BICYCLISTSIMPAIRED],
                            'DRIVERSIMPAIRED':[DRIVERSIMPAIRED],'TOTAL_TAXIS':[TOTAL_TAXIS],
                            'TOTAL_GOVERNMENT':[TOTAL_GOVERNMENT],'SPEEDING_INVOLVED':[SPEEDING_INVOLVED]})
        #df1 = pd.DataFrame.from_items(dat)
        df = pd.concat([df,dat])
    return(df)

df = pd.DataFrame()
df = getCrashAPI()
df.to_csv('originalCrash.txt',sep = '|', index = False)
df.to_csv('originalCrash.csv',sep = ',', index = False)
df = pd.read_csv('originalCrash.csv' , sep=',', encoding='latin1')

## Get level of cleanliness of each variable 
# check for NaN data
NaCount = {}
for col in df.columns:
    NaCount[col] = df[col].isnull().values.ravel().sum()
    #print('Numer of NaN entries in',col,'is',NaCount[col])

print(NaCount)
# Only addess has missing values
# check for noise values
noiseDat = {}
count = 0
# Check for variable ADDRESS. If the address is all digits or the length of the 
# address is <=6 then it's highly likely to be wrong data
# However, some of the address entries only contain highway such as I295. We consider
# those are not noise. Hwy is the list of all highways in DC
Hwy = {'66','395','695','295'}
for i in range(len(df.index)):
    if (df['ADDRESS'].iloc[i] is not None):
        if (any(hwy in str(df['ADDRESS'].iloc[i]) for hwy in Hwy)):
            continue
        if(not type(df['ADDRESS'].iloc[i]) ==str or 
           df['ADDRESS'].iloc[i].isdigit() or len(df['ADDRESS'].iloc[i])<=6):            
            count = count +1
noiseDat['ADDRESS'] = count

# Check for variable BICYCLISTSIMPAIRED.It is so extremely unlikely to have an 
# impaired cyclist that we don't really want put them into the study and we consider 
# all entries with 1 are noise values
count = 0
for i in range(len(df.index)):
    if (df['BICYCLISTSIMPAIRED'].iloc[i] is not None):
        if(not df['BICYCLISTSIMPAIRED'].iloc[i] == 0):
            count = count +1
noiseDat['BICYCLISTSIMPAIRED'] = count
# Check variable BICYCLISTSIMPAIRED for noise values
#print(pd.unique(df['BICYCLISTSIMPAIRED']))
# This variable only contains 0 and 1 so we could consider they all are not noise

# Then we check MAJORINJURIES_BICYCLIST,MINORINJURIES_BICYCLIST and FATAL_BICYCLIST
#print(pd.unique(df['MAJORINJURIES_BICYCLIST']))
#print(pd.unique(df['MINORINJURIES_BICYCLIST']))
#print(pd.unique(df['FATAL_BICYCLIST']))
# From the unique values, all three variables have reasonale values. So we want to check further
# Since TOTAL_BICYCLES is porvided in the data so we except to see number of major,minior 
# injuries and fatalities <= number of bicycles
count = 0
for i in range(len(df.index)):
    sumInjuries = df['MAJORINJURIES_BICYCLIST'].iloc[i]+df['MINORINJURIES_BICYCLIST'].iloc[i]
    +df['FATAL_BICYCLIST'].iloc[i]+df['UNKNOWNINJURIES_BICYCLIST'].iloc[i]
    if (sumInjuries > df['TOTAL_BICYCLES'].iloc[i]):
        count = count +1
#print(count)
# This number is 0
noiseDat['MAJORINJURIES_BICYCLIST'] = count
noiseDat['MINORINJURIES_BICYCLIST'] = count
noiseDat['FATAL_BICYCLIST'] = count
noiseDat['TOTAL_BICYCLES']=count
#print(pd.unique(df['MAJORINJURIES_DRIVER']))
#print(pd.unique(df['MINORINJURIES_DRIVER']))
#print(pd.unique(df['FATAL_DRIVER']))
# Same strategy with bicylist, find sum of major, minior injuries and fatalities 
# and see if that number <= number of vehicles in the accident
count = 0
for i in range(len(df.index)):
    sumInjuries = df['MAJORINJURIES_DRIVER'].iloc[i]+df['MINORINJURIES_DRIVER'].iloc[i]
    +df['FATAL_DRIVER'].iloc[i]++df['UNKNOWNINJURIES_DRIVER'].iloc[i]
    if (sumInjuries > df['TOTAL_VEHICLES'].iloc[i]):
        #print(df['TOTAL_VEHICLES'].iloc[i])
        count = count +1
#print(count)
noiseDat['MAJORINJURIES_DRIVER'] = count
noiseDat['MINORINJURIES_DRIVER'] = count
noiseDat['FATAL_DRIVER'] = count

# 
countFrom = 0
countReport = 0
for i in range(len(df.index)):
    if(not len(df['FROMDATE'].iloc[i]) ==24):
       countFrom=countFrom+1
    if(not len(df['REPORTDATE'].iloc[i]) ==24):
        countReport = countReport+1
        

noiseDat['FROMDATE'] =countFrom
noiseDat['REPORTDATE'] =countReport

# Check for lat and long. The boundary of DC is lat:38.9955 to 38.79 Long: -77.12 to -76.90
countLat = 0
countLong = 0
latNorth = 38.9955
latSouth = 38.79
longWest = -77.12
longEast = -76.9
for i in range(len(df.index)):
    if (df['LATITUDE'].iloc[i] > latNorth or df['LATITUDE'].iloc[i]<latSouth):
        countLat = countLat+1
    if (df['LONGITUDE'].iloc[i]<longWest or df['LONGITUDE'].iloc[i]>longEast):
        countLong = countLong+1
        
noiseDat['LATITUDE'] = countLat
noiseDat['LONGITUDE'] = countLong

# Check for noise values in TOTAL_VEHICLES
# Since this is dataset for car accidents, TOTAL_VEHICLES = 0 is noise value
count = 0
for i in range(len(df.index)):
    if (df['TOTAL_VEHICLES'].iloc[i]==0):
        count = count +1
noiseDat['TOTAL_VEHICLES'] =count
count = 0

for i in range(len(df.index)):
    sumInjuries = df['MAJORINJURIES_PEDESTRIAN'].iloc[i]+df['MINORINJURIES_PEDESTRIAN'].iloc[i]
    +df['FATAL_PEDESTRIAN'].iloc[i] +df['UNKNOWNINJURIES_PEDESTRIAN'].iloc[i]
    if (sumInjuries > df['TOTAL_PEDESTRIANS'].iloc[i]):
        count = count +1

noiseDat['MAJORINJURIES_PEDESTRIAN'] = count
noiseDat['MINORINJURIES_PEDESTRIAN'] = count
noiseDat['FATAL_PEDESTRIAN'] = count
noiseDat['TOTAL_PEDESTRIANS'] = count

# TOTAL_GOVERNMENT and TOTAL_TAXIS
count = 0
for i in range(len(df.index)):
    sumVehicle = df['TOTAL_GOVERNMENT'].iloc[i] + df['TOTAL_TAXIS'].iloc[i]
    if (df['TOTAL_VEHICLES'].iloc[i] < sumVehicle):
        count = count +1
        
noiseDat['TOTAL_GOVERNMENT'] = count
noiseDat['TOTAL_TAXIS'] = count

count = 0
for i in range(len(df.index)):
    if (df['TOTAL_VEHICLES'].iloc[i] < df['SPEEDING_INVOLVED'].iloc[i]):
        count = count +1
        
noiseDat['SPEEDING_INVOLVED'] = count


## From the description of the data, SPEEDING_INVOLVED indicates if the reporting 
## officer believed speeding was a factor in the crash. This doesn't necessarily 
## equate to participants being ticketed/cited for speeding. 
## In this case, it's reasonable to convert this attribute into a categorical attribute
## 0 means no speeding and 1 means speeding.
for i in range(len(df.index)):
    if (not df['SPEEDING_INVOLVED'].iloc[i] ==0):
        df['SPEEDING_INVOLVED'].iat[i] = 1

# Re-run and check if the quality improves 
count = 0
for i in range(len(df.index)):
    if (df['TOTAL_VEHICLES'].iloc[i] < df['SPEEDING_INVOLVED'].iloc[i]):
        count = count +1
print(count)



