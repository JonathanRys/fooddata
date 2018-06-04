import re
from list_tokenize import list_tokenize, translate_to_en_chars, strip_special_chars, trim_whitespace

def remove_special(file):
    input_file = open(file, "r", encoding="utf-8")
    data = input_file.read()
    input_file.close()

    data = list_tokenize(data)
    data = translate_to_en_chars(data, "fr")
    data = translate_to_en_chars(data, "es")
    data = strip_special_chars(data)
    data = trim_whitespace(data)

    output_file = open("output_" + file, "w", encoding="utf-8")
    for item in data:
        output_file.write(item + " ")
    output_file.close()


remove_special("foods.txt")
