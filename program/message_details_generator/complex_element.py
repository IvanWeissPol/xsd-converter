class complex_data():
    
    def __init__(self):
        self.Name = ""
        self.Type = ""
        self.Cardinality = ""
        self.Base_Type = ""
        self.Constraints = []
        self.Enumerations = []

class Complex_Element_Object():
    _height = 0    

    def get_height(self):
        return type(self)._height

    def set_height(self,val):
        type(self)._height = val

    height = property(get_height, set_height)

    def __init__(self):
        self.complex_data = complex_data()
        self.children = []
        self.parent = ""
        self.level = 1

    def add_children(self, child):
        child.parent = self
        child.level = self.level +1
        if child.level > self.height:
            self.height = child.level
        self.children.append(child)
        

    def print_tree2(self,level):
        spaces = "|  " * level
        prefix = spaces + "|__"
        print(prefix + self.complex_data.Name)
        if self.children:
            for child in self.children:
                child.print_tree2(level+1)
                
    def print_tree(self):
        level = 0
        spaces = "|  " * level
        prefix = spaces + "|__"
        print(prefix + self.complex_data.Name)
        if self.children:
            for child in self.children:
                child.print_tree2(level+1)

    def find_node(self,name):
        if self.complex_data.Name == name :
            return self
        else:
            name_list = name.split("_") 
            #typo in the xsd Measurement_Series should be MeasurementSeries
            #! add an error for new typos to know to add
            listOfTypos = ["Measurement", "Detail"]
            if(name_list[0] in listOfTypos ):
                aux = name_list[0] + "_" + name_list[1]
                name_list.remove(name_list[1])
                name_list.remove(name_list[0])
                name_list.insert(0,aux)
            if self.complex_data.Name in name_list:
                name_list.remove(self.complex_data.Name)
            name = "_".join(name_list)
            for child in self.children:
                parent = child.find_node(name)
                if parent != None:
                    return parent
        return None

