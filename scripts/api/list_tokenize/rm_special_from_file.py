import re
from list_tokenize import translate_to_en_chars, strip_special_chars

def remove_special(file):
    f = open(file, "r", encoding="utf-8")
    data = f.read()
    f.close()
    
    print(len(data))
    
    data = translate_to_en_chars._no_list(data, "fr")
    print(len(data))
    data = translate_to_en_chars._no_list(data, "es")
    print(len(data))
    data = strip_special_chars._no_list(data)
    print(len(data))
   



    f = open("output_" + file, "w", encoding="utf-8")
    f.write(data)
    f.close()



remove_special("foods.txt")
