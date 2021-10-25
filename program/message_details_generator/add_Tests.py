import pandas as pd
from os import listdir
from pandas.io import excel
import xlsxwriter
import openpyxl
from openpyxl.worksheet.dimensions import ColumnDimension

import sys
sys.path[0] += '\\..'

baseType_tests ={"string":["correct value","Invalid value","empty value","missing element"]
            ,"dateTime":["correct value","wrongDate","wrongOrderOfDate","empty"]
            ,"decimal":["correct value","negative","0","fractionalNumber","bigNumber","empty","1decimal","2decimal","3decimal","12decimal"]
            ,"integer":["correct value","negative","0","bigNumber","empty"]
            }
#if type contains key will add the list of test cases
Type_tests ={"Identifier":["unique ID","repeated ID"]
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




