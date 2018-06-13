import re
from tokenizer import translate_to_en_chars, strip_special_chars, trim_whitespace


def remove_special(file):
    input_file = open(file, "r", encoding="utf-8")
    data = input_file.read()
    input_file.close()

    # data = list_tokenize(data) # This is now done by the previous process
    data = data.split("\n")
    data = translate_to_en_chars(data, "all")
    data = strip_special_chars(data)
    data = trim_whitespace(data)
    data = [x for x in data if len(x) > 1]

    output_file = open("output_" + file, "w", encoding="utf-8")
    for item in data:
        output_file.write(item + " ")
    output_file.close()


if __name__ == '__main__':
    remove_special("converters/foods.txt")
