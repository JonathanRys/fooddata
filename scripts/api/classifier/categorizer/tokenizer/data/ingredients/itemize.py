import re

def itemize():
    with open('raw_ingredients.txt', "rt", encoding="utf-8") as f:
        data = f.read()

    data = re.split(r"[\"\']\, [\'\"]", data)

    with open('all_ingredients.txt', "wt", encoding="utf-8") as f:
        for item in data:
            f.write(item)

if __name__ == '__main__':
    itemize()
