import os
from spell_correct import correct

from multiprocessing import Process
from symspell_python import best_word, create_dictionary

import time

from spell_checker import SpellChecker
spell_checker = SpellChecker('data/dictionaries/spelling.dict')

symspell_dict = create_dictionary('data/dictionaries/spelling.dict')

dirname = os.path.dirname(__file__)

SORTED_INGREDIENTS = os.path.join(
    dirname, "data/ingredients/srtd_ingredients.txt")
FRUITS = os.path.join(dirname, "data/catagories/fruit.txt")

MATCHED = os.path.join(dirname, "data/matched.txt")
FOUND = os.path.join(dirname, "data/found.txt")
MISSPELED = os.path.join(dirname, "data/unknown.txt")


def read_data(file):
    print("Reading from " + file + "...")
    with open(file, "rt", encoding="utf-8") as f:
        data = f.read()

    return data.split("\n")


def write_data(file, data):
    print("Writing to " + file + "...")
    with open(file, "wt", encoding="utf-8") as f:
        for item in data:
            f.write(item + "\n")


def check_list(filename):
    ingredients = read_data(filename)

    matched = []
    found = []
    misspelled = []

    print("Checking the spelling of words...")
    for ingredient in ingredients:
        #best = best_word(ingredient)
        best = spell_checker.correct(ingredient)

        if best == None:
            misspelled.append(ingredient)

        elif ingredient == best:
            matched.append(ingredient)
        else:
            found.append(ingredient)

    write_data(MATCHED, matched)
    write_data(FOUND, found)
    write_data(MISSPELED, misspelled)

    print("done.")


if __name__ == '__main__':
    start_time = time.time()
    check_list(SORTED_INGREDIENTS)
    print("--- %s seconds ---" % (time.time() - start_time))
