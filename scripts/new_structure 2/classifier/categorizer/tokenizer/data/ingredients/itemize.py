import re

def itemize():
    with open('raw_ingredients.csv', encoding="utf-8") as f:
        data = f.read()

    data = re.split(r"[\"\']\, [\'\"]", data)

    with open('all_ingredients.txt', encoding="utf-8") as f:
        f.write(data)

if __name__ == '__main__':
    itemize()
