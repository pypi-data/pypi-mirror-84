#depend
#import pandas as pd
#import os


# # var
# path='./source/'

# #rename and filter
# file_columns=['create_time','channel','server_id','role_id','ip']


def con_sheets(path,file_columns):
    import pandas as pd
    import os

    #find all files
    files=os.listdir(path)
    
    #combine files
    list_file=[]
    for file_name in files:
        dic_data=pd.read_excel(path+file_name,sheet_name=None,header=None,dtype='object')

        #combine sheets 
        list_sheet=[]
        for sheet_name in dic_data:
            sheet=dic_data[sheet_name]
            list_sheet.append(sheet)
        df_data=pd.concat(list_sheet,axis=0,sort=False,ignore_index=True)

        #rename and filter
        df_data=df_data.rename(columns=dict(zip(range(len(file_columns)),file_columns)))
        df_data=df_data.dropna(how='all')
        df_data=df_data.loc[df_data[file_columns[0]]!=file_columns[0],:]
        
        list_file.append(df_data)
        
    df_files=pd.concat(list_file,axis=0,sort=False,ignore_index=True)
    
    return df_files