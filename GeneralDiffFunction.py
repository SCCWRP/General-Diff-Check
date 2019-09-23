import pandas as pd

#This is the path of data file 1
df1 = pd.read_excel("P:/PartTimers/DuyNguyen/Python Practice/pythonpractice/unittest1.xlsx")

#This is the path of data file 2
df2 = pd.read_excel("P:/PartTimers/DuyNguyen/Python Practice/pythonpractice/unittest2.xlsx")



def Input_dataframes(df1,df2,mergingcolumns):
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
    duplicateRowsDF1 = df1[df1.duplicated()]
    
    #print(Test1)
    
    #Find the duplicates in data 2 
    #print('These are the duplicates in 2')
    duplicateRowsDF2 = df2[df2.duplicated()]
    
    #print(Test2)
    print('The following are duplicate records: ')
    print('DATAFRAME 1:',duplicateRowsDF1)
    print('DATAFRAME 2:',duplicateRowsDF2)
    # Now we can find the records that are in 1 but not 2, and vice versa.
    print('The following record is only in one dataframe: ')
    set(list(zip(*[df1[col] for col in df1]))) - set(list(zip(*[df2[col] for col in df2])))
    In1notIn2 = pd.DataFrame(set(list(zip(*[df2[col] for col in df2]))) - set(list(zip(*[df1[col] for col in df1]))),columns = df1.columns)
    
    print('DATAFRAME 1(not in DATAFRAME 2):')
    print(In1notIn2 )
    set(list(zip(*[df2[col] for col in df2]))) - set(list(zip(*[df1[col] for col in df1])))
    In2notIn1 = pd.DataFrame(set(list(zip(*[df2[col] for col in df2]))) - set(list(zip(*[df1[col] for col in df1]))),columns = df1.columns)

    print('DATAFRAME 2(not in DATAFRAME 1):')
    print(In2notIn1)


   
    #We can assume that df1 and df2 have the same column names at this point in the code , and we check  for mismatch
    #I merge them together, drop the uncommon values between them
    merged = pd.merge(df1.drop_duplicates(), df2.drop_duplicates(), on = mergingcolumns, how = 'inner', suffixes = ('_1','_2'))
    #I drop the duplicate rows, keep the first occurence
    for colname in df1.columns:
        if colname not in mergingcolumns:
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
    #merged.to_excel('P:\PartTimers\DuyNguyen\Python Practice\pythonpractice\SOmethingtosee.xlsx')
   
            
Input_dataframes(df1,df2,['stationid','fishspecies'])
