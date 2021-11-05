import pandas as pd 
import numpy as np
import sys
import xml.etree.cElementTree as ET



from pandas.io.pytables import AppendableFrameTable
sys.path[0] += '\\..'
import paths
from os import error, listdir

def get_line_that_contains(searched_string,lines):
    for line  in lines:
        if searched_string in line :
            return lines.index(line)




def make_xml(test_cases_folder_path):
    name = "AllocationVolumeRevisionRequest"
    folder = paths.xmls_base_folder_path
    path = folder + "\\base_" + name + ".xml"
    base_file = open(path,"r")

    all_lines = base_file.readlines()

    element_path= "EDSNBusinessDocumentHeader/ContentHash"
    element_path = element_path.split("/") 
    auxList = []
    for element in element_path:
        element = "ccma:" + element
        auxList.append(element)
    element_path = "/".join(auxList)

    new_value  = "aaaaaaaaaaaaaaa"
    prefix = "ccma:"
    tree = etree.parse(path)
    tree = tree.getroot()
    test_elements = ["ccma:EDSNBusinessDocumentHeader" ,"ccma:EDSNBusinessDocumentHeader/ccma:ContentHash","ccma:EDSNBusinessDocumentHeader/ccma:ConversationID","ccma:EDSNBusinessDocumentHeader/ccma:Destination"]
    for element in test_elements :
        test1 = tree.findall(element,tree.nsmap)
        print(test1)
    test_elements = ["EDSNBusinessDocumentHeader" ,"ContentHash","ConversationID","Destination"]
    for child in tree:
        print(child.tag, child.attrib)
        for element in test_elements:
            test1 = child.findall(element,tree.nsmap)
    for element in test1:
        print (element.text)    

    print("pause")
#make_xml(test_cases_folder_path= paths.test_cases_folder_path)