import copy
from lxml import etree
from typing import ContextManager, Optional
import pandas as pd 
import numpy as np
import sys
import shutil
import os

from pandas.io.pytables import AppendableFrameTable
sys.path[0] += '\\..'
import paths
from os import error, listdir


def create_xml(has_child_list,rows,col_list,name,default_value_list):
    #gets the rows data and writes it to the xml
    path = paths.xmls_folder_path +"\\base\\base_" + name + ".xml"
    f = open(file=path,mode="a")
    get_xml_row_data(has_child_list=has_child_list, col_list=col_list,rows=rows,previous_col=0,f=f,default_value_list=default_value_list)
    f.close()

def get_xml_row_data(has_child_list,rows,col_list,previous_col,f,default_value_list):
    if len(col_list)!=0:
        has_child = has_child_list.pop(0)
        element = rows.pop(0)
        col = col_list.pop(0)
        default_value = default_value_list.pop(0)
        write_xml_Row(has_child_list= has_child_list,has_child=has_child, col=col, col_list=col_list, element=element, previous_col= previous_col, rows=rows,f=f, default_value_list=default_value_list,default_value=default_value)

def write_xml_Row(has_child_list,rows,col_list,previous_col,has_child,element,col,f,default_value, default_value_list):
    tabs = "\t"*col
    prefix = tabs + "<ccma:" + element + " > "
    if(str(default_value) == 'nan'):
        default_value = ""
    
    value = str(default_value)
    sufix = "</ccma:"+ element + ">"
    
    line = prefix
    if len(col_list) >=0:
        if has_child:
            if col == 0:
                line=line.replace(">", "")
                value +=">"
                line+=value
            if len(col_list) >0:
                if col < col_list[0]:
                    value = ""
            line+="\n"
            f.write(line)
            #while has kids
            if len(col_list) >0:
                while col < col_list[0]:
                    get_xml_row_data( has_child_list=has_child_list, col_list=col_list, rows= rows, previous_col=previous_col,f=f,default_value_list= default_value_list)
                    if len(col_list)==0:
                        break
                #
            line=tabs + sufix
            line+="\n"
            f.write(line)
        else:
            line+=value
            line+=sufix
            line+="\n"
            f.write(line)
    else:
        x=1

def get_base_Xml(excel_name):
    message_details_folder_path = paths.message_details_folder_path
    folder = listdir(message_details_folder_path)
    name = excel_name.rsplit("_",1)[1]
    name = name.split(".")[0]
    for excel in folder:
        if name in excel:
            path = message_details_folder_path + "\\" + excel
            df = pd.read_excel(path)
            
            BaseType = df['BaseType']
            default_element_values = df['Default Values']
            #remove the columns that are not needed
            df = df[df.columns.difference(['Type'])]
            df = df[df.columns.difference(['Cardinality'])]
            df = df[df.columns.difference(['Constraints'])]
            df = df[df.columns.difference(['Enumerations'])]
            df = df[df.columns.difference(['tests'])]
            df = df[df.columns.difference(['BaseType'])]
            df = df[df.columns.difference(['Default Values'])]
            

            element_points_in_Excel = list(zip(*np.where(df.notnull())))
            element_list = []
            has_child_list = []
            col_list = []
            default_value_list = []
            for row ,point,type_aux,default_value in zip(df.iterrows(),element_points_in_Excel,BaseType.iteritems(),default_element_values.iteritems()):
                col_list.append(point[1])
                element_list.append(row[1][point[1]])
                default_value_list.append(default_value[1])
                if not pd.isnull(type_aux[1]):
                    has_child_list.append(False)
                else:
                    has_child_list.append(True)
                
            #write the xml file
            create_xml(has_child_list=has_child_list, col_list=col_list,rows=element_list,name=name,default_value_list=default_value_list)
            excel_df = pd.DataFrame()
            columns=list(df.columns.values)

def create_cases(excel_name,row):
    row = row
    name = excel_name.rsplit("_",1)[1]
    name = name.split(".")[0]
    element = row['Element']
    allowed_values = row['Enumerations']
    test_message = row['Test message']
    optional = row['optional']
    allowed_values = row['Enumerations']            #predifined values
    values_restrictions = row['restricted values']  #restrictions or rules that values must follow
    test_values = row['tested values']              #values that will be tested
    element_path = row['path']

    test_values = test_values.replace("[", "")
    test_values = test_values.replace("]", "")
    test_values = test_values.replace("'", "")
    test_values = test_values.replace('"', "")
    test_values = test_values.split(", ")


    path = paths.xmls_folder_path +"\\base\\base_" + name + ".xml"
    test_cases_folder = make_test_case_folder(path,test_message)
    #list_of_lines_containing_element = find_element_in_xml(element=element,f=f)
    for value in test_values:
        #generates a copy of the base file
        new_case_path = make_test_case(test_cases_folder,test_values.index(value))
        #modifies the copy
        if value == "deleteElement":
            print("deleteElement")
            delete_block(child_of_element_to_be_duplicated_path=element_path,new_case_path=new_case_path)
        elif value == "addElement":
            print("addElement")
            #add_block(child_of_element_to_be_duplicated_path=element_path,new_case_path=new_case_path)
        elif value == "repeated_ID":
            #duplicate_element_box(child_of_element_to_be_duplicated_path=element_path,new_case_path=new_case_path)
            print("repeated_ID")
        elif value == "repeated_ID_2":
            print("wrongOrderOfDate")
        else:
            modify_test_case(new_case_path,element_path,value)
        
        
        
    os.remove(test_cases_folder + "\\base.xml")

def modify_test_case(new_case_path,element_path,value):
    element_path = element_path.split("/") 
    auxList = []
    for element in element_path:
        element = "ccma:" + element
        auxList.append(element)
    auxList.pop(0)
    element_path = "/".join(auxList)
    if element_path == 'ccma:Measurement_Series/ccma:DateAndOrTime/ccma:endDateTime':
        print("pause")
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    test1 = tree.findall(element_path,tree.nsmap)
    test1[0].text = value
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)

def delete_block(new_case_path,child_of_element_to_be_duplicated_path):
    prefix = "ccma:"
    child_of_element_to_be_duplicated_path = child_of_element_to_be_duplicated_path.split("/")
    child_of_element_to_be_duplicated_path.pop(0)
    child_of_element_to_be_duplicated_path[0] = prefix + child_of_element_to_be_duplicated_path[0]
    separator = "/"+prefix
    child_of_element_to_be_duplicated_path = separator.join(child_of_element_to_be_duplicated_path)
    # child_of_element_to_be_duplicated_path = "a:EDSNBusinessDocumentHeader/ccma:DateAndOrTime/ccma:startDateTime"
    element_to_change  = child_of_element_to_be_duplicated_path.rsplit("/")[1]
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    test1 = tree.findall(child_of_element_to_be_duplicated_path,tree.nsmap)
    child = test1[0]
    parrent = child.getparent()
    parrent.remove(child)
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)

def duplicate_element_box(new_case_path,child_of_element_to_be_duplicated_path):
    child_of_element_to_be_duplicated_path = "ccma:Measurement_Series/ccma:DateAndOrTime/ccma:startDateTime"
    element_to_change  = child_of_element_to_be_duplicated_path.rsplit("/")[1]
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    test1 = tree.findall(child_of_element_to_be_duplicated_path,tree.nsmap)
    child = test1[0]
    parrent = child.getparent()
    grandparent = parrent.getparent()

    
    new_block = copy.deepcopy(parrent)
    new_element = new_block.findall("ccma:startDateTime",tree.nsmap)
    #change the value from the new element
    new_element = new_element[0]
    new_element.text = "new values aaaaaaaaaaaaaaaaaaaaaaaaa"
    
    #add new element to tree
    grandparent.append(new_block)
    #save the new tree
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)
    


def make_test_case(test_cases_folder,number):
    name = test_cases_folder.rsplit("\\",1)[1]
    new_case_path = test_cases_folder + "\\" + name + "_" + str(number) + ".xml"
    base_case_path = test_cases_folder + "\\base.xml"
    shutil.copyfile(base_case_path, new_case_path)
    return new_case_path

def find_element_in_xml(element,f):
    list_of_lines_containing_element = []
    # content = f.readline()
    # lines = [x for x in content if element in content]

    for line in f:
        if element in line:
            list_of_lines_containing_element.append(line)
    return list_of_lines_containing_element 

def make_test_case_folder(path,test_message):
    test_case_path = path.rsplit("\\",1)[1]
    test_case_path = test_case_path.replace("base_", "")
    name = test_case_path.replace(".xml", "")

    test_folder = paths.xmls_cases_folder_path + "\\" + name
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    test_message_no_point = test_message.split(".")[0]
    test_folder = test_folder + "\\" + test_message_no_point
    test_folder = test_folder.replace("\n", "")
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

    test_case_path = test_folder + "\\" + "base.xml"
    shutil.copyfile(path, test_case_path)
    return test_folder

def make_test_cases_xmls(test_cases_folder_path):
    #get the test cases excel files 
    folder = listdir(test_cases_folder_path)
    for excel in folder:

        #make the datarame from the test cases excel file
        path = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(path,skiprows=1)

        #remove the columns that are not needed
        df = df[df.columns.difference(["Status"])]
        df = df[df.columns.difference(['Error'])]
        df = df[df.columns.difference(['Observations'])]
        df = df[df.columns.difference(['BaseType'])]
        df = df[df.columns.difference(['Case'])]
        excel_df = pd.DataFrame()
        #read the rows from the test cases excel file
        # only when elements are not empty a test case will be created based on the test values
        # when elements are empthy it means the row is a visual row for people (not machine) 
        # example 
        # Element	Test message	Status	Error	Observations	optional	BaseType	restricted values	Enumerations	Case	tested values	Default values
        # AllocationVolumeRevisionRequest												
        # EDSNBusinessDocumentHeader												

        for row in df.iterrows():
            row = row[1]
            if not pd.isnull(row["Element"]):
                if  row["Element"] != "Element":
                    create_cases(row=row,excel_name=excel)
            
        #save the excel
        path = paths.xmls_folder_path + "\\" + "title" + ".xlsx"
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        excel_df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()

def make_base_xmls(test_cases_folder_path):
    #get the test cases excel files 
    folder = listdir(test_cases_folder_path)
    for excel in folder:
        #make the baseXml file
        base_Xml = get_base_Xml(excel)



#remove element