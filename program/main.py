import message_details_generator.tree_to_excel as message_details_generator
import test_cases_generator.test_cases as test_cases_generator
import message_details_generator.add_Tests as add_Tests
from xml_generator.base_xml_generator import make_test_cases_xmls,make_base_xmls
import paths as paths

stay_in_program = True
while stay_in_program:
    print("chose what to do:")
    print("1. make excels from xsd")
    print("2. make test cases")
    print("3. make base xmls")
    print("4. make xmls")
    print("5. exit")
    case = input()
    if case == "1":
        message_details_generator.make_excels_from_xsd(folder_Of_xsd=paths.xsd_folder_path)
        add_Tests.add_Tests(message_details_folder_path=paths.message_details_folder_path)
    elif case == "2":
        test_cases_generator.make_test_cases(message_details_folder_path=paths.message_details_folder_path)
    elif case == "3":
        print("are you shure?")
        print("creating new base xml will recuier you to manualy set the namespace of all the base xml")
        print("before creating the test cases xmls")
        print("1. yes")
        print("2. no")
        sure = input()
        if sure == "1":
            make_base_xmls(test_cases_folder_path=paths.test_cases_folder_path)
    elif case == "4":
        make_test_cases_xmls(test_cases_folder_path=paths.test_cases_folder_path)
    elif case == "5":
        stay_in_program = False
    stay_in_program = False
