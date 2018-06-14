import re
import os
from tokenizer import translate_to_en_chars, strip_special_chars, trim_whitespace


def remove_special(file):
    if not os.path.exists(file) or not os.path.isfile(file):
        return False

    with open(file, "rt", encoding="utf-8") as f:
        data = f.read()

    # data = list_tokenize(data) # This is now done by the previous process
    data = data.split("\n")
    data = translate_to_en_chars(data, "all")
    data = strip_special_chars(data)
    data = trim_whitespace(data)
    data = [x for x in data if len(x) > 1]

    output_file = open(file, "wt", encoding="utf-8")
    for item in data:
        output_file.write(item + " ")
    output_file.close()

    return True


if __name__ == '__main__':
    remove_special("./data/spelling_scraper/foods.txt")
