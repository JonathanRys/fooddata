import re
from list_tokenize import special_chars

# Decorator
def use_list(func):
    def wrapper(list_to_process):
        output_list = []

        for item in list_to_process:
            result = func(item)

            # Remove empty items
            if len(result):
                output_list.append(result)
 
        return output_list
    
    return wrapper

# Utilities
def list_tokenize(list_to_split):
    return [x.strip() for x in re.split(special_chars.patterns["list_boundries"], list_to_split)]

@use_list                 
def translate_to_en_chars(string, lang = "es"):
    if not lang in special_chars.special_chars:
        raise KeyError("No pattern found for mapping \"" + lang + "\" -> \"en\".")
    
    char_map = str.maketrans(special_chars.special_chars[lang])
    return string.translate(char_map)

@use_list
def strip_special_chars(string):
    return re.sub(special_chars.re_pattern("non_alpha_numeric"), "", string)

@use_list
def trim_whitespace(string):
    # Removes all leading, trailing or duplicated whitespace and converts all whitespace to spaces
    return re.sub(special_chars.re_pattern("whitespace"), " ", string).strip()

@use_list
def lower_case(string):
    return string.lower()



# Tests
def test():

    alphabet = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"]
    punctuation = "’'()[]{}<>:,‒–—―…!.«»-‐?‘’“”;/⁄␠·&@*\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※"
    itemized_list = "Here is one, this is a\nother; try  this and that or how    about these/those"
    es_chars = ["á", "é", "í", "ó", "ú", "ü", "ñ", "Á", "É", "Í", "Ó", "Ú", "Ü", "Ñ", "¿", "¡"]
    spaces_in_odd_places = ["\t    Do    you  ", "   know", " \the\t\tmuffi\n", "ma\n?   " ]

    # Test list_tokenize
    result_list = list_tokenize(itemized_list)
    assert len(result_list) == 7
    assert result_list[0] == "Here is one"
    assert result_list[6] == "those"

    # Test translate_to_en_chars
    result_list = translate_to_en_chars(es_chars)
    assert len(result_list) == 14
    assert result_list[0] == "a"
    assert result_list[13] == "N"

    # Test strip_special_chars
    result_list = strip_special_chars(punctuation)
    assert len(result_list) == 2
    assert result_list[0] == "-"
    assert result_list[1] == "_"

    # Test trim_whitespace
    result_list = trim_whitespace(spaces_in_odd_places)
    assert len(result_list) == 4
    assert result_list[0] == "Do you"
    assert result_list[2] == "he muffi"
    assert result_list[3] == "ma ?"

    # Test lower_case
    result_list = lower_case(alphabet)
    assert len(result_list) == 38
    assert result_list[0] == "a"
    assert result_list[25] == "z"
    assert result_list[28] == "3"
    assert result_list[37] == "-"


    print("All tests passed.")

# Run tests by default
if __name__ == '__main__':
    test()
