import re
import os

INPUT_FILE = 'raw_ingredients.txt'
OUTPUT_FILE = 'all_ingredients.txt'


def itemize():
    if not os.path.exists(INPUT_FILE) or not os.path.isfile(INPUT_FILE):
        from .ingredients import get_source_data
        get_source_data()

    with open(INPUT_FILE, "rt", encoding="utf-8") as f:
        data = f.read()

    data = re.split(r"[\"\']\, [\'\"]", data)

    with open(OUTPUT_FILE, "wt", encoding="utf-8") as f:
        for item in data:
            f.write(item)

    return True


if __name__ == '__main__':
    itemize()
