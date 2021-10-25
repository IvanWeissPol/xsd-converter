import shutil
import os
from re import L
import pandas as pd
import xlsxwriter
from os import listdir
import sys
sys.path.append("..")
sys.path.append("...")
import paths
import message_details_generator.xsd_converter_to_tree as xsd_converter_to_tree
import message_details_generator.complex_element as complex_element

#traverse the tree and add each node to the list of list (each list in the list represents a column in the final excel)
# might not be the best way but its "a" way ja ja ja
def traverse_tree(node:complex_element ,listOLists):
    for cont in range (1,node.height+1):
        dflevel = "L" + str(cont)    
        listOLists[dflevel].append("")       

    dflevel = "L" + str(node.level)
    listOLists[dflevel].pop()
    listOLists[dflevel].append(node.complex_data.Name)       
    listOLists["Type"].append(node.complex_data.Type)       
    listOLists["Cardinality"].append(node.complex_data.Cardinality)       
    listOLists["BaseType"].append(node.complex_data.Base_Type)       
    listOLists["Constraints"].append(node.complex_data.Constraints)
    listOLists["Enumerations"].append(node.complex_data.Enumerations)
    #do the same for each child of the node        
    for child in node.children:
        traverse_tree(child,listOLists)

#make an excel for each xsd in the folder
def make_excels_from_xsd(folder_Of_xsd):
    folder_path = folder_Of_xsd
    folder = listdir(folder_path)
    for element in folder:
        if element.endswith(".xsd"):
            element_path = folder_path + "\\" + element
            done_prosesing_path = folder_path + "\\done\\" + element
            name = element_path.split(".")[0].rsplit("\\")[1]
            #generate the tree from the xsd
            root = xsd_converter_to_tree.get_tree(xsd_path=element_path)
            
            path = paths.message_details_folder_path + "\\mesage_details_" + name + ".xlsx"
            listOLists = {}
            
            for cont in range (1,root.height+1):
                dflevel = "L" + str(cont)    
                listOLists[dflevel] = [] 
#            listOLists = {"L1":[],"L2":[],"L3":[],"L4":[],"L5":[],"Cardinality":[],"Type":[],"BaseType":[],"Constraints":[],"Enumerations":[]}
            listOLists["Type"] = []
            listOLists["Cardinality"] = []
            listOLists["BaseType"] = []
            listOLists["Constraints"] = []
            listOLists["Enumerations"] = []
            #make the list of lists and turn it in to an excel sheet
            traverse_tree(root,listOLists)
            df = pd.DataFrame(data=listOLists)
            writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1',index=False)
            writer.save()
            shutil.move(element_path, done_prosesing_path)
            

