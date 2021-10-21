import pandas as pd 
import sys
sys.path[0] += '\\..'
from paths import *
from os import error, listdir

def add_title(df ,title):
    row = pd.Series(title)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    return df
def add_subtitle(df ,subtitle):
    row = pd.Series(subtitle)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    row = pd.Series(["#","Element","Case","Test message","Status","Error","Observations","optional","restricted values","tested values"])
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    
    return df

def add_test_cases(df ,row,columns,title,cont):
    list_of_cases = row.tests
    list_of_cases = list_of_cases.split(" ")
    for string in columns:
        if string.startswith('L') and not pd.isnull(row[string]):
            element = row[string]
    optional = "false"
    if(row.Cardinality =="0..1"):
        optional = "true"
    status = ""
    error = ""
    observation = ""
    restricted_values = row.Constraints
    for case in list_of_cases:
        test_message = title + "_" + str(cont)
        if case == 'make2WithSameID':
            test_message = test_message+"_1 \n" + test_message+"_2"
        new_row = [cont,element,case,test_message,status,error,observation,optional,restricted_values]
        row_df = pd.DataFrame([new_row])
        df = pd.concat([df,row_df],ignore_index=True)
        cont +=1
    return cont,df


folder = listdir(message_details_folder_path)
for excel in folder:
    path = message_details_folder_path + "\\" + excel
    df = pd.read_excel(path)
    
    df = df[df.columns.difference(['Type'])]
    df = df[df.columns.difference(['BaseType'])]
    excel_df = pd.DataFrame()
    columns=list(df.columns.values)
    test_cases_cont = 0
    for row in df.iterrows():
        row = row[1]
        if not(pd.isnull(row.L1)) or not(pd.isnull(row.L2)):
            if not(pd.isnull(row.L1)):
                excel_df = add_title(df=excel_df, title=row.L1)
                title = row.L1
            if not(pd.isnull(row.L2)):
                excel_df = add_subtitle(df=excel_df,subtitle=row.L2)
        else:
            if not(pd.isnull(row.tests)):
                test_cases_cont ,excel_df = add_test_cases(df=excel_df, row=row, columns=columns, title=title, cont=test_cases_cont)
    path = test_cases_folder_path + "\\test_cases_" + title + ".xlsx"
    writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
    excel_df.to_excel(writer, sheet_name='Sheet1',index=False)
    writer.save()