from pprint import pprint

import EU4FileParser

example_string_to_tokenize = ''' 
a = { 
    name = "Tes//la"
    #test comment
    value = "Москва"  
    test_object = {
        obj_key = obj_value
        tears_of_joy = 777.777
    }
    test_object = {
        obj_key_second = obj_value_second
        tears_of_joy_second = 111.111
    }
    test_object = {
        obj_key_third = obj_value_third
        tears_of_joy_second = 111.111
    }
    test_object = {
        obj_key_fourth = obj_value_fourth
        tears_of_joy_second = 111.111
    }
}

b = {
    test = testb
    test_objectss = {
        obj_key_second = obj_value_second
        tears_of_joy_second = 111.111
    }
}


'''

parser = EU4FileParser.EU4Parser()
result = parser.parse(example_string_to_tokenize)
pprint(result)
