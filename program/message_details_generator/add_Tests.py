import pandas as pd
from os import listdir
from pandas.io import excel
import xlsxwriter
import openpyxl
from openpyxl.worksheet.dimensions import ColumnDimension

import sys
sys.path[0] += '\\..'

baseType_tests ={
    "string":["correct_value" ,"Invalid_value" ,"empty_value" ,"missing_element"],
    "dateTime":["correct_value" ,"wrongDate" ,"wrongOrderOfDate" ,"empty" ,"missing_element"],
    "decimal":["correct_value" ,"empty" ,"1_decimal" ,"2_decimal" ,"3_decimal" ,"12_decimal" ,"missing_element"],
    "integer":["correct_value" ,"empty" ,"missing_element"]
                }
#if type contains key will add the list of test cases
Type_tests ={"Identifier":["unique_ID","repeated_ID"]
}

def add_Tests(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for element in folder:
        
        #path where the message details excels are stored
        path = message_details_folder_path + "\\" + element
        df = pd.read_excel(path)

        #all the test cases for each element base type tests + type tests
        df["tests"] = ""
        for key in baseType_tests:
            df.loc[df["BaseType"] == key,"tests"] = ' '.join(baseType_tests[key])
        for key in Type_tests:
            df.loc[df["Type"].str.contains(key,na=False),"tests"] = df["tests"] +" " +  ' '.join(Type_tests[key])

        #save the generated document
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()




