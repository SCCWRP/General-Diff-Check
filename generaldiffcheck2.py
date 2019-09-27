import os, time,datetime
import pandas as pd
from pandas import DataFrame
import numpy as np
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
import csv
import xlrd
# I create engine to read into the database
eng = create_engine("postgresql://smcread:1969$Harbor@192.168.1.17:5432/smc")
#Assign panda dataframes from the tables in SQL server 
sqlcommand = pd.read_sql("SELECT * FROM lu_station",eng)




'''
# bring in the stations completeness file - we are checking to see which areaweight fields are filled 
df = pd.ExcelFile('/Users/pauls/Desktop/Projects/Bight18/FishInvert/OCSD/fish1bio.xlsx') 
df_tab_names = df.sheet_names 
df1 = df.parse('Sheet1')  

# bring in the stations completeness file - we are checking to see which areaweight fields are filled 
df = pd.ExcelFile('/Users/pauls/Desktop/Projects/Bight18/FishInvert/OCSD/fish2bio.xlsx') 
df_tab_names = df.sheet_names 
df2 = df.parse('Sheet1')
'''

def compare_dataframes(df1, df2):
    mergingcols = ['stationid','sampleid','sampledate','samplingorganization','trawlnumber','fishspecies','sizeclass','abundancequalifier','abundance','anomaly','diversityindexexclude','Comments']
    #print("The following are duplicate records in dataframe 1")
    #print(df1[df1.duplicated()==True].to_string())
 
    #print("\n\n\n\n\n")
    #print("The following are duplicate records in dataframe 2")
    #print(df2[df2.duplicated()==True].to_string())
 
    '''
    print("\n\n\n\n\n")
    if set(df1.columns) != set(df2.columns):
        print("The dataframes do not have matching column names")
        print("df1 columns")
        print(df1.columns)
        print("df2.columns")
        print(df2.columns)
        #return
    '''

    mergingcols = list(df1.columns)
    #print(mergingcols)
    #print(list(df1))
    #print(list(df2))
  
    df1['record_exists'] = True
    df2['record_exists'] = True
    in1not2 = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']
    #print(in1not2)
 
    #in1not2 = in1not2[in1not2.record_exists_2.isnull()]
 
    #in2not1 = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only']
    #in2not1 = in2not1[in2not1.record_exists_1.isnull()]

    in1not2.to_csv('/Users/pauls/Desktop/Projects/Bight18/FishInvert/OCSD/biomass-df1vsdf2.csv') 
    print("The following records are in only the first dataframe")
    print(in1not2.to_string())
    print("\n\n\n\n\n")
 
 
    #print("The following record is in only the second dataframe")
    #print(in2not1)

