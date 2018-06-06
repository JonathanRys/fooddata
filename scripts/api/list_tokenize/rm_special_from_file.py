import re
from list_tokenize import list_tokenize, translate_to_en_chars, strip_special_chars, trim_whitespace

def remove_special(file):
    input_file = open(file, "r", encoding="utf-8")
    data = input_file.read()
    input_file.close()

    # data = list_tokenize(data) # This is already done for me by the previous process
    data = data.split("\n")
    data = translate_to_en_chars(data, "all")
    data = strip_special_chars(data)
    data = trim_whitespace(data)
    data = [x for x in data if len(x) > 1]

    output_file = open("output_" + file, "w", encoding="utf-8")
    for item in data:
        output_file.write(item + " ")
    output_file.close()


remove_special("foods.txt")
