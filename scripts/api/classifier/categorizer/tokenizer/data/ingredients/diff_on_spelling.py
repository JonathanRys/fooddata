import os

dirname = os.path.dirname(__file__)

SPELLING = os.path.join(dirname, "all_spelling.txt")
ALL_WORDS = os.path.join(dirname, "srtd_ingredients.txt")
OUTPUT_FILE = os.path.join(dirname, "output.txt")


with open(SPELLING, 'rt', encoding='utf-8') as f:
    spelling_words = f.read().split("\n")

with open(ALL_WORDS, 'rt', encoding='utf-8') as f:
    all_words = f.read().split("\n")

diff = [x for x in all_words if x.lower() not in spelling_words and x.capitalize() not in spelling_words]

with open(OUTPUT_FILE, 'wt', encoding='utf-8') as f:
    for x in diff:
        f.write(x + '\n')
