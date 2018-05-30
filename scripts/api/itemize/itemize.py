import re
from special_chars import special_chars, patterns, re_pattern

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
def itemize_list(list_to_split):
    return [x.strip() for x in re.split(patterns["list_boundries"], list_to_split)]

@use_list                 
def translate_to_en_chars(string, lang = "es"):
    if not lang in special_chars:
        raise KeyError("No pattern found for mapping \"" + lang + "\" -> \"en\".")
    
    char_map = str.maketrans(special_chars[lang])
    return string.translate(char_map)

@use_list
def strip_special_chars(string):
    return re.sub(re_pattern("non_alpha_numeric"), "", string)

@use_list
def trim_whitespace(string):
    # Removes all leading, trailing or duplicated whitespace and converts all whitespace to spaces
    return re.sub(re_pattern("whitespace"), " ", string).strip()

@use_list
def lower_case(string):
    return string.lower()



# Tests
def test():

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-"
    punctuation = "’'()[]{}<>:,‒–—―…!.«»-‐?‘’“”;/⁄␠·&@*\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※"
    itemized_list = "Here is one, this is a\nother; try  this and that or how    about these/those"
    es_chars = ["á", "é", "í", "ó", "ú", "ü", "ñ", "Á", "É", "Í", "Ó", "Ú", "Ü", "Ñ", "¿", "¡"]
    spaces_in_odd_places = [" Hi", "There  ", "    do    you  ", "   know", " the\t\tmuffi\n", "man?   " ]

    # Test itemize_list
    result_list = itemize_list(itemized_list)
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
    assert len(result_list) == 6
    assert result_list[2] == "do you"
    assert result_list[4] == "the muffi"

    # Test lower_case
    result_list = lower_case(alphabet)
    assert len(result_list) == 38
    assert result_list[0] == "a"
    assert result_list[25] == "z"

    print("All tests passed.")

# Run tests by default
if __name__ == '__main__':
    test()
