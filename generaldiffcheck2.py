import pandas as pd
import numpy as np
import copy

def compare_dataframes(df1, df2):
    print("The following are dupliacte records in dataframe 1")
    for row in df1[df1.duplicated()==True].iterrows():
        print(row)
        print('\n')
   
    print("\n\n\n\n\n")
    print("The following are dupliacte records in dataframe 2")
    for row in df2[df2.duplicated()==True].iterrows():
        print(row)
        print('\n')

    print("\n\n\n\n\n")
    if set(df1.columns) != set(df2.columns):
        print("The dataframes do not have matching column names")
        print("df1 columns")
        print(df1.columns)
        print("df2.columns")
        print(df2.columns)
        return

    mergingcols = list(df1.columns)

    df1['record_exists'] = True
    df2['record_exists'] = True

    in1not2 = pd.merge(df1, df2, on = mergingcols, how = 'left', suffixes = ('_1','_2'))
    in1not2 = in1not2[in1not2.record_exists_2.isnull()]

    in2not1 = pd.merge(df1, df2, on = mergingcols, how = 'right', suffixes = ('_1','_2'))
    in2not1 = in2not1[in2not1.record_exists_1.isnull()]

    print("The following record is in only the first dataframe")
    for row in in1not2.iterrows():
        print(row)
        print('\n')

    print("\n\n\n\n\n")


    print("The following record is in only the second dataframe")
    for row in in2not1.iterrows():
        print(row)
        print('\n')

    
    
