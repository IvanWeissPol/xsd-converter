from logging import root
import xmlschema
from pprint import pprint
from Simple_Element import Simple_Element_Object
from complex_element import Complex_Element_Object
def get_tree(xsd_path ):
    xs = xmlschema.XMLSchema(xsd_path)
    dict = xs.to_dict(xsd_path)
    simple_Element_List = []
    #for every type in the simpleType subdict add the element to the list 
    for simpleType in dict["xsd:simpleType"]:
        aux_SEO = Simple_Element_Object()
        aux_SEO.Name = simpleType["@name"] 
        #get the list of restrictions 
        for Constraints in simpleType["xsd:restriction"]:
            #base
            if Constraints == "@base":
                aux_SEO.Type = simpleType["xsd:restriction"][Constraints]
            #valid values for the elements
            elif Constraints == 'xsd:enumeration':
                if len(simpleType["xsd:restriction"][Constraints]) == 1:
                    possible_value = str(simpleType["xsd:restriction"][Constraints]["@value"])
                    aux_SEO.possible_allowed_value.append(possible_value)
                else:
                    for possible_allowed_value in simpleType["xsd:restriction"][Constraints]:
                        possible_value += str(possible_allowed_value["@value"])
                        aux_SEO.possible_allowed_value.append(possible_value)
            #anything else
            else:
                Constraints_aux = Constraints.replace("xsd:" ,"")
                Constraints_aux += " = "
                Constraints_aux += str(simpleType["xsd:restriction"][Constraints]["@value"])
                aux_SEO.restriction.append(Constraints_aux)    
        simple_Element_List.append(aux_SEO)

    #make the complex type tree from the xsd
    base_type = ""
    restrictions =[]
    possible_allowed_value_list = [] 
    child_name_in_bfs = []
    #create the root
    complexType = dict["xsd:complexType"]
    root = Complex_Element_Object()
    root.complex_data.Name = complexType[0]["@name"] 
    min = complexType[0]["xsd:sequence"]["@minOccurs"]
    max = complexType[0]["xsd:sequence"]["@maxOccurs"]
    cardinality  = str(min) + ".." + str(max) 
    root.complex_data.Cardinality = cardinality
    if complexType[0].get("@type"):
        root.complex_data.Type = complexType[0]["@type"].split(":")[1]
        base_type = ""
        restrictions =[]
        possible_allowed_value_list = [] 
        for element in simple_Element_List:
            if root.complex_data.Type == element.Name:
                base_type = element.Type.rsplit(":")[1]
                restrictions = element.restriction
                possible_allowed_value_list = element.possible_allowed_value
                break
        root.complex_data.Base_Type = base_type
        root.complex_data.Constraints = restrictions
        root.complex_data.Enumerations = possible_allowed_value_list
    for child in complexType[0]["xsd:sequence"]["xsd:element"]:
        child_node = Complex_Element_Object()
        child_node.complex_data.Name = child["@name"] 
        min = child["@minOccurs"]
        max = child["@maxOccurs"]
        cardinality  = str(min) + ".." + str(max) 
        child_node.complex_data.Cardinality = cardinality
        if child.get("@type"):
            child_node.complex_data.Type = child["@type"].split(":")[1]
            base_type = ""
            restrictions =[]
            possible_allowed_value_list = [] 
            for element in simple_Element_List:
                if child_node.complex_data.Type == element.Name:
                    base_type = element.Type.rsplit(":")[1]
                    restrictions = element.restriction
                    possible_allowed_value_list = element.possible_allowed_value
                    break
            child_node.complex_data.Base_Type = base_type
            child_node.complex_data.Constraints = restrictions
            child_node.complex_data.Enumerations = possible_allowed_value_list
        root.add_children(child_node)
        child_name_in_bfs = child_node.complex_data.Name
        
    #create the tree
    for cont in range(1,len(complexType)):
        aux_CEO = complexType[cont]
        node = Complex_Element_Object()
        node.complex_data.Name = aux_CEO["@name"]
        if 'BEAreaLocation' == aux_CEO["@name"]:
            print("stop")
        node = root.find_node_in_tree(node.complex_data.Name)
        node.complex_data.Cardinality = str(aux_CEO["xsd:sequence"]["@minOccurs"]) + ".." + str(aux_CEO["xsd:sequence"]["@maxOccurs"])
        try:
            node.complex_data.Type = aux_CEO["@type"].split(":")[1]
            base_type = ""
            restrictions =[]
            possible_allowed_value_list = [] 
            for element in simple_Element_List:
                if node.complex_data.Type == element.Name:
                    base_type = element.Type.rsplit(":")[1]
                    restrictions = element.restriction
                    possible_allowed_value_list = element.possible_allowed_value
                    break
            node.complex_data.Base_Type = base_type
            node.complex_data.Constraints = restrictions
            node.complex_data.Enumerations = possible_allowed_value_list
        except TypeError:
            pass
        except KeyError:
            pass
        
        #nodes of tree with only 1 child
        #!add an error for new uncheked nodes with only 1 child
        ListOfNodeWithOneChild = ['FlowDirection','MarketEvaluationPoint','MarketRole',"BEAreaLocation"]
        if 'PayloadBEEnergyTimeSeries' == node.complex_data.Name:
            print("stop")
        if not (node.complex_data.Name in ListOfNodeWithOneChild):
            for child in aux_CEO["xsd:sequence"]["xsd:element"]:
                child_node = Complex_Element_Object()
                child_node.complex_data.Name = child["@name"] 
                min = child["@minOccurs"]
                max = child["@maxOccurs"]
                cardinality  = str(min) + ".." + str(max) 
                child_node.complex_data.Cardinality = cardinality
                if child.get("@type"):
                    child_node.complex_data.Type = child["@type"].split(":")[1]
                    base_type = ""
                    restrictions =[]
                    possible_allowed_value_list = [] 
                    for element in simple_Element_List:
                        if child_node.complex_data.Type == element.Name:
                            base_type = element.Type.rsplit(":")[1]
                            restrictions = element.restriction
                            possible_allowed_value_list = element.possible_allowed_value
                            break
                    child_node.complex_data.Base_Type = base_type
                    child_node.complex_data.Constraints = restrictions
                    child_node.complex_data.Enumerations = possible_allowed_value_list
                node.add_children(child_node)
        else:
            child_node = Complex_Element_Object()
            child_node.complex_data.Name = aux_CEO["xsd:sequence"]["xsd:element"]["@name"] 
            min = aux_CEO["xsd:sequence"]["xsd:element"]["@minOccurs"]
            max = aux_CEO["xsd:sequence"]["xsd:element"]["@maxOccurs"]
            cardinality  = str(min) + ".." + str(max) 
            child_node.complex_data.Cardinality = cardinality
            if aux_CEO["xsd:sequence"]["xsd:element"].get("@type"):
                child_node.complex_data.Type = aux_CEO["xsd:sequence"]["xsd:element"]["@type"].split(":")[1]
                base_type = ""
                restrictions =[]
                possible_allowed_value_list = [] 
                for element in simple_Element_List:
                    if child_node.complex_data.Type == element.Name:
                        base_type = element.Type.rsplit(":")[1]
                        restrictions = element.restriction
                        possible_allowed_value_list = element.possible_allowed_value
                        break
                child_node.complex_data.Base_Type = base_type
                child_node.complex_data.Constraints = restrictions
                child_node.complex_data.Enumerations = possible_allowed_value_list
            node.add_children(child_node)
    return root
    
