import re
from special_chars import special_chars, patterns, re_pattern

def itemize_list(list_to_split):
    return [x.strip() for x in re.split(patterns["list_boundries"], list_to_split)]
                 
def translate_to_en_chars(string, lang = "es"):
    if not lang in special_chars:
        raise KeyError("No pattern found for mapping \"" + lang + "\" -> \"en\".")
    
    char_map = str.maketrans(special_chars[lang])
    return test_string.translate(char_map)

def strip_special_chars(string):
    return re.sub(re_pattern("non_alpha_numeric"), "", string)

def trim_whitespace(string):
    # Removes all leading, trailing or duplicated whitespace
    return re.sub(re_pattern("whitespace"), " ", string)

def lower_case(string):
    return string.lower()



def test():
    test_string = "’'()[]{}<>:,‒–—―…!.«»-‐?‘’“”;/⁄␠·&@*\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※"

    return re.sub(re_pattern("punctuation"), "", test_string)

# print(itemize_list("Hi there, do you and your friend want to play; or not?"))

# "[’'()[\]{}<>:,‒–—―…!.«»\-‐?‘’“”;/⁄␠·&@*\\\•^¤¢$€£¥₩₪†‡°¡¿¬#№%‰‱¶′§~¨_|¦⁂☞∴‽※]"
# print(test())

