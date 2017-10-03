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