import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import copy
import re



eng = create_engine("postgresql://smcread:1969$Harbor@192.168.1.17:5432/smc")
database_data = pd.read_sql("SELECT * FROM tbl_siteeval WHERE login_agency = 'VCWPD' AND created_date = '2019-08-13 09:38:49' ",eng)
user_data = pd.read_excel("C:\\Users\\GisUser\\Desktop\\user_data.xls")
user_data.columns = map(str.lower, user_data.columns)


for col in user_data.columns:
    if "date" in col:
        user_data[col].fillna(pd.Timestamp('1950/01/01'),inplace =True)

#This function is to compare the two data frame regardless of their sizes
#Adjust the directory to see the output files        
primarykeys = ['stationcode','drawcode','programcode','agencycode','evaldate']

def compare_and_highlight(df1,df2,primarykeys):
    mergingcols = primarykeys
    #database_data.drop(columns = [col for col in database_data.columns if col not in user_data.columns],inplace = True)

    merged = pd.merge(
                df1, 
                df2,
                on = mergingcols,
                how = 'outer',
                suffixes = ('_old','')
                )

    merged['change_type'] = merged.apply(
            lambda x: 
                "addition" 
                # if all of the "old" column values are null, then the user added a new record
                if all(
                        [pd.isnull(x[f'{col}_old']) for col in df1.columns if col not in mergingcols ]) 
                else "deletion"
                # if all of the "new" columns have null values, then the user deleted a record
                if all(
                    [pd.isnull(x[f'{col}']) for col in df1.columns if col not in mergingcols  ]
                    )
                else "modification"
                # if any of the old column values are different from the new columns values, it is a modified record
                if any(
                        [x[f'{col}'] != x[f'{col}_old'] for col in df1.columns if col not in mergingcols ]
                        )
        # if it doesn't meet any above case, there is no change and we return a Nonetype object
            else None 

        # don't forget that axis = 1 since the args passed to the lambda function are rows of the dataframe
            , axis = 1 
            )

    #Extract the information that we want - either the records are added, modified, or deleted
    #primarykeys are in 2 not in 1
    add_records =  merged[merged['change_type'] == "addition"]
    #primarykeys are in both df, but there are some modifications
    modified_records = merged[merged['change_type'] == "modification"]
    #primarykeys are in 1 not in 2
    delete_records = merged[merged['change_type'] == "deletion"]

    modified_records.replace("", np.NaN, inplace = True)

    #Create the list of columns to loop
    loopcols = [col for col in user_data.columns if col not in mergingcols]

    #Adding the "same" column to modified_records
    for col in loopcols:
        modified_records[f'{col}_same'] = modified_records.apply(
                lambda x: (x[f'{col}'] == x[f'{col}_old']) | (all(map(pd.isnull,[x[f'{col}'], x[f'{col}_old']] ) ) ), 
                axis = 1
                )

    #Reorder the columns in modified_records for easy reading. 
    modified_records = modified_records.sort_index(axis = 1)
    ordered_columns = mergingcols + [col for col in modified_records.columns if col not in mergingcols]
    modified_records = modified_records[ordered_columns]
    modified_records.drop(columns = ['change_type'],inplace = True)



    cols_to_check = [col for col in modified_records.columns if "_same" in col]
    cols_to_drop = []
    for col in cols_to_check:
        if all(modified_records[col]) == True:
            cols_to_drop.append(col.replace("_same",""))
            cols_to_drop.append(col.replace("_same","_old"))
            cols_to_drop.append(col)
            #cols_to_drop = cols_to_drop + cols_to_check
    modified_records.drop(columns = cols_to_drop, inplace = True)
    modified_records.reset_index(drop = True, inplace = True)
    #changed_cols = [
    #        col for col in modified_records.columns if (not all(modified_records[col].tolist())) and (bool(re.search("_same", col)))
    #    ]
    #
    ##
    #for col in changed_cols:
    #    col = col.replace("_same","")
    #    modified_records[f"{col}_old"] = modified_records.apply(lambda x: str(x) + " " if modified_records[f"{col}_same"] == False else x,axis= 1 )
    #    


    changed_indices = []

    for col in filter(lambda x: bool(re.search("_same",x)), modified_records.columns):

        modified_records.apply(
                
                lambda x:

                    changed_indices.append(

                (x.name + 1, modified_records.columns.get_loc(re.sub("_same","_old",col)))
                
                )

            if x[col] == False
            
            else np.NaN, # end 1st arg

            axis = 1 # 2nd arg

        )

    # after grabbing coordinates of what we need, drop that "same" column
        modified_records.drop(col, axis = 1, inplace = True)
    writer = pd.ExcelWriter("P:\\PartTimers\\DuyNguyen\\Projects\\GeneralDiffCheckMaster\\General-Diff-Check\\output\\MODIFIED.xlsx", engine = 'xlsxwriter')

    modified_records.to_excel(writer, sheet_name = "modified",index = False)

    workbook = writer.book

    color = workbook.add_format({'bg_color':'#FF0000'})

    worksheet = writer.sheets["modified"]

 

    # coord is a tuple of the coordinates of cells that were changed, and need to be highlighted

    for coord in changed_indices:

        worksheet.conditional_format(

            coord[0], coord[1], coord[0], coord[1],

            {

                'type': 'no_errors',

                'format': color

            }

        )

    writer.save()

#Write the ADDTION records to excel
#add_records.drop(columns = [col for col in add_records.columns if "_old" in col ],inplace = True)
#directory2 = 'P:\\PartTimers\\DuyNguyen\\Projects\\GeneralDiffCheckMaster\\General-Diff-Check\\output\\ADDITION.xlsx'
#writer2 = pd.ExcelWriter(directory2, engine = 'xlsxwriter')
#add_records.to_excel(writer2,index = False)
#writer2.save()