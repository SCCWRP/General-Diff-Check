import pandas as pd

#This is the path of data file 1
#df1 = pd.read_excel("P:/PartTimers/DuyNguyen/Python Practice/pythonpractice/unittest1.xlsx")
df1 = pd.read_excel("sampledata/Bight18_Trawl_Data_1_reformatted.xlsx", sheet_name = 'trawlinvertebrateabundance')

df1.invertspecies = df1.invertspecies.apply(lambda x: str(x).strip())


#This is the path of data file 2
#df2 = pd.read_excel("P:/PartTimers/DuyNguyen/Python Practice/pythonpractice/unittest2.xlsx")
df2 = pd.read_excel("sampledata/Bight18_Trawl_Data_2_reformatted.xlsx", sheet_name = 'trawlinvertebrateabundance')
df2.invertspecies = df2.invertspecies.apply(lambda x: str(x).strip())



def compare_dataframes(df1,df2,mergingcolumns):
    #df1 is the fist dataframe, df2 is the second dataframe, mergingcolumns: the columns we are gonna merge them on
    # mergingcolumns must be a list
    #Check to make sure the names of the columns are the same
    #If they are the same, we are going to merge the columns that we want
    
    df1cols = set(df1.columns)
    df2cols = set(df2.columns)
    print(df1cols)
    print(df2cols)
    if df1cols != df2cols:
        print("The two dataframes do not have matching column names")
        return
    #Find the duplicates in data 1 
    print('These are the duplicates in 1')
    duplicateRowsDF1 = df1[df1.duplicated(subset = mergingcolumns)]
    duplicateRowsDF1.to_csv("output/duplicaterowsDF1.csv")
    
    #Find the duplicates in data 2 
    #print('These are the duplicates in 2')
    duplicateRowsDF2 = df2[df2.duplicated(subset = mergingcolumns)]
    duplicateRowsDF2.to_csv("output/duplicaterowsDF2.csv")

    #print(Test2)
    print('The following are duplicate records: ')
    print('DATAFRAME 1:',duplicateRowsDF1)
    print('DATAFRAME 2:',duplicateRowsDF2)
    
    # Now we can find the records that are in 1 but not 2, and vice versa.
    # Previous idea of just getting the values of the columns where the records were only in onee but not the other 
    #  I found to not be helpful for me when I was trying to hunt down the duplicates
    #  More efficient way is to left and right join and check for null values
    #  This is the ""more efficient method" I was trying to tell Duy about, but we did not have time to talk about it at that time
    
    # The reason I do this is hard to explain in writing
    df1['record_exists'] = True
    df2['record_exists'] = True
    
    in1not2 = pd.merge(df1, df2, on = mergingcolumns, how = 'left')
    in2not1 = pd.merge(df1, df2, on = mergingcolumns, how = 'right')

    in1not2 = in1not2[in1not2.record_exists_y.isnull()]
    in2not1 = in2not1[in2not1.record_exists_x.isnull()]

    in1not2.to_csv("output/in1not2.csv")
    in2not1.to_csv("output/in2not1.csv")

    df1.drop('record_exists', axis = 1, inplace = True)
    df2.drop('record_exists', axis = 1, inplace = True)


    #We can assume that df1 and df2 have the same column names at this point in the code , and we check  for mismatch
    #I merge them together, drop the uncommon values between them
    merged = pd.merge(
            df1.drop_duplicates(subset = mergingcolumns), 
            df2.drop_duplicates(subset = mergingcolumns),
            on = mergingcolumns,
            how = 'inner',
            suffixes = ('_1','_2')
        )

    #I drop the duplicate rows, keep the first occurence
    for colname in df1.columns:
        if colname not in mergingcolumns:
            print("merged")
            print(merged)
            merged[str(colname) + " Check"] = merged.apply(lambda x: (x[str(colname) + '_1'] == x[str(colname) + '_2']) | ((pd.isna(x[str(colname) + '_1'])) & (pd.isna(x[str(colname) + '_2']))), axis=1)
    
            
           # writer = pd.ExcelWriter('P:\PartTimers\DuyNguyen\Python Practice\pythonpractice\GeneralDiffCheck.xlsx', engine = 'xlsxwriter')
            #merged.to_excel(writer, sheet_name = 'Check for values')
            #In1notIn2.to_excel(writer, sheet_name = 'In Set 1 not in Set 2 list')
            #In2notIn1.to_excel(writer, sheet_name = 'In Set 2 not in Set 1 list')
            #writer.save()
            #writer.close()    
            
        
            #merged.to_excel('P:\PartTimers\DuyNguyen\Python Practice\pythonpractice\GeneralDiffCheck.xlsx')
            #print("This is the table where we show which values are mismatched")
            #print(merged)
    merged.to_csv('output/mismatches.csv')
   
            
compare_dataframes(df1,df2,['stationid','invertspecies', 'trawlnumber', 'sampleid','samplingorganization'])
