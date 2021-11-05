import pandas as pd 
import sys
sys.path[0] += '\\..'
import paths
from os import listdir
import paths 
number_of_titles = 0

list_of_test_values = {
    "string":{
        "correct_value":["aaaa","bbbb"],
        "Invalid_value":[1,0,2,3,0.1,0.2,-0.1,-0.2],
        "empty_value":[""],
        "missing_element":["deleteElement"]
    },
    "dateTime":{
        "correct_value":[11/12/2000,1/1/2000,11/11/2000],
        "wrongDate":[2000/11/11,11/2000/11,50/50/2000],
        "wrongOrderOfDate":["wrongOrderOfDate"],
        "empty":[""],
        "missing_element":["deleteElement"]
    },
    "decimal":{
        "correct_value":[-5,-4,-3,0,1,2,3,0.1,-0.1,-10000,10000],
        "empty":[""],
        "1_decimal":[1.1],
        "2_decimal":[1.12],
        "3_decimal":[1.123],
        "12_decimal":[1.1321657132],
        "missing_element":["deleteElement"]
    },
    "integer":{
        "correct_value":[-1,-2,-3,-4,-10000,1,2,3,4,1000000],
        "empty":[""],
        "missing_element":["deleteElement"]
    },
    "Identifier":{
        "unique_ID":["unique_ID"],
        "repeated_ID":["repeated_ID"]
    }
}

def add_title(df ,title):
    global number_of_titles
    number_of_titles += 1
    row = pd.Series(["#","Element","path","Test message","Status","Error","Observations","optional","BaseType","restricted values","Enumerations","Case","default tested values","extra values to test"])
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    row = pd.Series(title)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    return df

def add_subtitle(df ,subtitle):
    global number_of_titles
    number_of_titles += 1
    row = pd.Series(subtitle)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    #row bellow every subtitle to understand what each column is
    row = pd.Series(["#","Element","path","Test message","Status","Error","Observations","optional","BaseType","restricted values","Enumerations","Case","default tested values","extra values to test"])
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    return df

def add_test_cases(df ,row,added_subtitles,columns,title,cont,excel_row,element_path):
    list_of_cases = row.tests
    list_of_cases = list_of_cases.split(" ")
    element_path_list = list(element_path.values())
    element_path_list = list(filter(("").__ne__, element_path_list))
    element_path_string = "/".join(element_path_list)
    element = element_path_list[-1]

    # add all other info from row
    optional = "false"
    if(row.Cardinality =="0..1"):
        optional = "true"
    status = ""
    error = ""
    observation = ""
    BaseType = row['BaseType']
    Enumerations = row["Enumerations"]
    restricted_values = row.Constraints
    
    #make a test case for each case
    for case in list_of_cases:
        if not "ID" in case:
            test_values = list_of_test_values[row.BaseType][case]    
        else:
            test_values = list_of_test_values["Identifier"][case]    
        
        
        if excel_row != 6:
            if added_subtitles:
                number = '=INDIRECTO(DIRECCION(FILA()-3,COLUMNA()))+1'
                added_subtitles = False
            else:
                number = '=INDIRECTO(DIRECCION(FILA()-1,COLUMNA()))+1'
        else:
            number = 0
            added_subtitles = False
        test_message = '=CONCATENAR(INDIRECTO(DIRECCION(3,1)),"_" ,INDIRECTO(DIRECCION(FILA(),COLUMNA()-3)))'
        new_row = [number,element,element_path_string,test_message,status,error,observation,optional,BaseType,restricted_values,Enumerations,case,test_values]
        row_df = pd.DataFrame([new_row])
        df = pd.concat([df,row_df],ignore_index=True)
        cont +=1
        excel_row +=1
    return excel_row,cont,df

def make_test_cases(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for excel in folder:
        path = message_details_folder_path + "\\" + excel
        df = pd.read_excel(path)
        
        #remove the columns that are not needed
        df = df[df.columns.difference(['Type'])]

        excel_df = pd.DataFrame()
        columns=list(df.columns.values)
        test_cases_cont = 0
        #read the rows
        element_path = {}
        aux_col = []
        for col in columns:
            if col.startswith('L'):
                aux_col.append(col)
        excel_row = 2
        added_subtitles = False
        for row in df.iterrows():
            row = row[1]
            if not(pd.isnull(row.L1)) or not(pd.isnull(row.L2)):
                if not(pd.isnull(row.L1)):
                    excel_df = add_title(df=excel_df, title=row.L1)
                    title = row.L1
                    element_path["L1"] = row.L1
                    excel_row +=2
                if not(pd.isnull(row.L2)):
                    excel_df = add_subtitle(df=excel_df,subtitle=row.L2)
                    added_subtitles =True
                    element_path["L2"] = row.L2
                    excel_row +=2
            else:
                #make the element path
                for col in aux_col:
                    if not pd.isnull(row[col]):
                        element_path[col] = row[col]
                        index = aux_col.index(col)
                        for pos in range(index+1,len(aux_col)):
                            element_path[aux_col[pos]] = ""
                            
                    
                    if not(pd.isnull(row.tests)) and not(pd.isnull(row[col])):
                        excel_row,test_cases_cont ,excel_df = add_test_cases(df=excel_df,added_subtitles=added_subtitles, row=row, columns=columns, title=title, cont=test_cases_cont, excel_row=excel_row,element_path=element_path)
                        added_subtitles = False

                    
        #save the excel
        path = paths.test_cases_folder_path + "\\test_cases_" + title + ".xlsx"
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        excel_df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()


# make_test_cases(paths.message_details_folder_path)