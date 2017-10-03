import requests
import pandas as pd
import numpy as np

locList = list()
# Location at national arboretum
locList.append('USC00186350')
# Location at dalecavlia reservior
locList.append('USC00182325')

dateList = list()
yr = list()
yr.append('2013')
yr.append('2014')
yr.append('2015')
yr.append('2016')
for i in range(len(yr)):
    dateList.append('startdate='+yr[i]+'-01-01&enddate='+yr[i]+'-03-31')
    dateList.append('startdate='+yr[i]+'-04-01&enddate='+yr[i]+'-06-30')
    dateList.append('startdate='+yr[i]+'-07-01&enddate='+yr[i]+'-09-30')
    dateList.append('startdate='+yr[i]+'-10-01&enddate='+yr[i]+'-12-31')    

#date = {'startdate=2013-01-01&enddate=2013-04-30','startdate=2013-05-01&enddate=2013-08-31',
#        'startdate=2013-09-01&enddate=2013-12-31'}
df = pd.DataFrame()
for i in range(len(dateList)):
    for k in range(len(locList)):
        BaseURL='https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&limit=1000&stationid=GHCND:'+locList[k]+'&units=standard&'+dateList[i]
        URLPost ={'token':'ekzgryaLzmqpLvYuHCERiUvLLGthmyJk'}
        response=requests.get(BaseURL,headers =URLPost)
        jsontxt = response.json()

        for j in range(len(jsontxt['results'])):
            date = jsontxt['results'][j]['date']
            value = jsontxt['results'][j]['value']
            datType = jsontxt['results'][j]['datatype']
            val = {'Date': [date],'Value':[str(value)],'DataType':[datType],'Location':[locList[k]]}
            dat = pd.DataFrame.from_dict(val)
            df = pd.concat([df,dat])
    
loc = 'US1VAFX0063'
dateList = list()
dateList.append('startdate=2013-07-08&enddate=2013-12-31')
dateList.append('startdate=2014-01-31&enddate=2014-06-30')
dateList.append('startdate=2014-07-01&enddate=2014-12-31')
dateList.append('startdate=2015-01-31&enddate=2015-06-30')
dateList.append('startdate=2015-07-01&enddate=2015-12-31')
dateList.append('startdate=2016-01-31&enddate=2016-06-30')
dateList.append('startdate=2016-07-01&enddate=2016-12-31')
for i in range(len(dateList)):
    BaseURL='https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&limit=1000&stationid=GHCND:'+loc+'&units=standard&'+dateList[i]
    URLPost ={'token':'ekzgryaLzmqpLvYuHCERiUvLLGthmyJk'}
    response=requests.get(BaseURL,headers =URLPost)
    jsontxt = response.json()
    for j in range(len(jsontxt['results'])):
        date = jsontxt['results'][j]['date']
        value = jsontxt['results'][j]['value']
        datType = jsontxt['results'][j]['datatype']
        val = {'Date': [date],'Value':[str(value)],'DataType':[datType],'Location':[loc]}
        dat = pd.DataFrame.from_dict(val)
        df = pd.concat([df,dat])
        
        
df.to_csv('weatherOri.txt',sep = '|', index = False)
df.to_csv('weatherOri.csv',sep = ',', index = False)

df = pd.read_csv('weatherOri.csv' , sep=',', encoding='latin1')
col = pd.unique(df[df.columns[0]]).tolist()
col.append('Location')
col.append('Date')
dfNew = pd.DataFrame(columns = col)
# subset the big dataframe into 3 small ones based on the location
dfLocUSC00186350 = df[df['Location'] == 'USC00186350']
# sort  the subset by date 
dfLocUSC00186350 =dfLocUSC00186350.sort_values(by=['Date'])
len(pd.unique(dfLocUSC00186350['Date']))
dateList = pd.unique(dfLocUSC00186350['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    dfAtDate = dfLocUSC00186350[dfLocUSC00186350['Date']==date]
    datType = pd.unique(dfAtDate['DataType']).tolist()
    dat = {'Date':[date], 'Location': ['USC00186350']}
    for j in range(len(datType)):
        dat.update({datType[j]:[dfAtDate[dfAtDate['DataType'] ==datType[j]].iloc[0]['Value']]})
    dat = pd.DataFrame.from_dict(dat)
    dfNew = pd.concat([dfNew,dat])

dfLocUSC00182325 = df[df['Location'] == 'USC00182325']
# sort  the subset by date 
dfLocUSC00182325 =dfLocUSC00182325.sort_values(by=['Date'])
len(pd.unique(dfLocUSC00182325['Date']))
dateList = pd.unique(dfLocUSC00182325['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    dfAtDate = dfLocUSC00182325[dfLocUSC00182325['Date']==date]
    datType = pd.unique(dfAtDate['DataType']).tolist()
    dat = {'Date':[date], 'Location': ['USC00182325']}
    for j in range(len(datType)):
        dat.update({datType[j]:[dfAtDate[dfAtDate['DataType'] ==datType[j]].iloc[0]['Value']]})
    dat = pd.DataFrame.from_dict(dat)
    dfNew = pd.concat([dfNew,dat])

dfLocUS1VAFX0063 = df[df['Location'] == 'US1VAFX0063']
# sort  the subset by date 
dfLocUS1VAFX0063 =dfLocUS1VAFX0063.sort_values(by=['Date'])
len(pd.unique(dfLocUS1VAFX0063['Date']))
dateList = pd.unique(dfLocUS1VAFX0063['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    dfAtDate = dfLocUS1VAFX0063[dfLocUS1VAFX0063['Date']==date]
    datType = pd.unique(dfAtDate['DataType']).tolist()
    dat = {'Date':[date], 'Location': ['US1VAFX0063']}
    for j in range(len(datType)):
        dat.update({datType[j]:[dfAtDate[dfAtDate['DataType'] ==datType[j]].iloc[0]['Value']]})
    dat = pd.DataFrame.from_dict(dat)
    dfNew = pd.concat([dfNew,dat])

# Delete all noise attributes 
del dfNew['DAPR']
del dfNew['MDPR']
del dfNew['SNWD']
del dfNew['TOBS']
del dfNew['WESD']
del dfNew['WESF']
del dfNew['WT01']
del dfNew['WT03']
del dfNew['WT04']
del dfNew['WT06']
del dfNew['WT11']

dfNew.to_csv('weatherAfterMerge.txt',sep = '|', index = False)
dfNew.to_csv('weatherAfterMerge.csv',sep = ',', index = False)

            

